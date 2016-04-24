<h1>What are proxies: </h1>
<p>"In computer networks, a proxy server is a server (a computer system or an application) that acts as an intermediary for requests from clients seeking resources from other servers. A client connects to the proxy server, requesting some service, such as a file, connection, web page, or other resource available from a different server and the proxy server evaluates the request as a way to simplify and control its complexity. Proxies were invented to add structure and encapsulation to distributed systems. Today, most proxies are web proxies, facilitating access to content on the World Wide Web and providing anonymity." <a href="https://en.wikipedia.org/wiki/Proxy_server"><span>Wikipedia</span></p></a>
<br>
<p>Setting up a proxy is fairly simple and today I am going to teach you how to do it: </p>
<p>But first, let's say you randomly found a proxy like this one: "<b>1.2.3.4:123</b>", later in the tutorial, we will see you need a port number to setup the proxy, but where is it?<br>Whenever you see an address like that, the number after the colon(:) is the port number, so in this case, the port to be used is 123.</p>
<p>Fun fact: Most routers, if not all of them have around 65,000 ports for two protocols(TCP and UDP).</p>
<p>Let's start: </p>
<ol>
<h1>Choosing a proxy: </h1>
<li>Websites like freeproxylists.net let you choose from a variety of filters, giving you an easier search for a proxy.<img src="https://i.gyazo.com/fd4703025fe9e04fd5fc6dd77d911be2.png"/>
<li>In this example, we are going to use this website.
<li>Choose a country close to the one you live in, know how it lags when you connect to people far away from you and it doesn't lag when they are close to you? That's the line of thought you should follow.
<li>The port filter is to be left empty if you are going to choose a place with few servers.<img src="https://i.gyazo.com/97d00d5c39a8beabd916f72d5ea1c519.png"/><p>No brazilian servers with the port 1000</p>
<li>HTTP or HTTPS: <br>Well, HTTP means "Hypertext Transfer Protocol", the file transfer part is for transfering the hypertext(HTML) page to your browser.<br>HTTPS means "Hypertext Transfer Protocol Secure" so, it's a bit self-explanatory.
<li>Proxy anonimity: Mess with the filter as long as you don't use a "Not anonymous" proxy, because that would have no use...<br>Anonymous is meh security and high anonymous severely decreases the chances of being traced.
<li>Uptime basically means the time the proxy server has been up without errors and rebooting, so, a proxy with 100% of uptime has never been shut off.<br> In my example, we will leave the uptime filter untouched.
<li>Response and Transfer: Green = Good; Yellow = Okay; Red = Bad; Colors apply to both :P<br>A proxy connection with red transfer and response will cause lag and connection issues.
<li>Warning: Proxies may go down at random, if it appears that you have no internet connection, the proxy server is probably down, you should now use another proxy setting(preferably the system defaults), wait until the proxy is back up again(Which is a bit stupid) or, choose another proxy.
</ol>
<ol>
<h1>Firefox: </h1>
<p>Now we chose our proxy we'll set it up:<br>Head into options -> Advanced(Wizard hat) -> Network<br>Click "Settings..." beside Configure how Firefox connects to the Internet</p><img src="https://i.gyazo.com/05f9a5a0e622e7ad35460cae4f9a4b09.png"/>
<li>It'll probably be set to use the default system settings, so toggle Manual configuration.
<li>Fill in the proxy information(IP address) and the port, preferably toggle to use this proxy for all protocols.
<li>The "No proxy for: " can be changed to specify which websites will not see you as your proxy server, but as your real IP address(Separate with commas(<b>,</b>)).
<ul>
<li>It is by default set to not use a proxy to localhost and 127.0.0.1(Separated with a comma might I add), because they are... You, your own computer, some softwares like Construct 2(for creating games) test your game projects on localhost:50000 which is localhost(You):port.
</ul>
<li>After that, press "Ok" and you have a proxy!
</ol>
