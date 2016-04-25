Pre-reqs
======
Make sure you have Virtualbox installed before continuing.
The rest of this document assumes you have installed
Virtualbox and (optionally) the Virtualbox Extension Pack
for your OS.


Vagrant Setup
=======
1. Install [vagrant](http://www.vagrantup.com/)
2. Install vagrant-hostmanager with ```vagrant plugin install vagrant-hostmanager```
2. Clone this repository `git clone git://github.com/jeethridge/ncaplite-vagrant`
3. Run `vagrant up`
4. Connect your spark client to developer@ncaplite.loc


Udpating your hosts file
======
The preferred method is to do this automatically using a tool. I've chosen to go with this project:

https://github.com/smdahlen/vagrant-hostmanager

Which can be installed by calling

```
vagrant plugin install vagrant-hostmanager
```

This should automatically up date you hosts file when you call ```vagrant up```
*Note that you'll have to use sudo enter your password to give permission to edit the
hosts file during provisioning*

If for some reason you'd rather update hosts file manually:
http://www.howtogeek.com/howto/27350/beginner-geek-how-to-edit-your-hosts-file/

you'll want to add this entry:



Using Spark
======
All the folks on the project up to this point seem to be using the Spark client
for manual testing, so I jumped on the bandwagon. You can get the Spark client here:

http://www.igniterealtime.org/projects/spark/

*You should be able to ignore the rest of this section if you installed
vagrant-hostmanager*

If automatic discovery doesn't work you can use the following workaround.
you must specify the server IP address in the Advanced options for the Spark client.
The default configuration for the Vagrant box is an IP of:

```
10.10.100.4
```

Of course, you'll also have to specify this host address as an argument
when you run the NCAP.
This IP is an arbitrary choice right now.
I just wanted an IP address that was unlikely to be used on a given developer machine.


Prosody Installation
======
I combined the info in these two articles and put in my own hostname
in the appropriate fields. The install consists mostly of defaults with a few
minor tweaks. The setup and user creation is taken care of automatically
in the provisioning.sh script.

1. http://arstechnica.com/information-technology/2014/03/how-to-set-up-your-own-private-instant-messaging-server/

2. https://www.debian-administration.org/article/700/Using_the_prosody_xmpp/chat_server

Accounts
======
There are three accounts set up on the server by default. These are:
|User | Pass|
|-----|-----|
|developer@ncaplite.loc | mypassword|
|ncap@ncaplite.loc      | mypassword|
|unittest@ncaplite.loc  | mypassword|

###About the accounts

**developer@ncaplite.loc** is intended for prototyping, developer spikes, and general manual hankey-pankey

**unittest@ncaplite.loc** is the client account you'll want to use in your unit testing. The assumption for now in the tests is a single connected client. This is obviously a stupid assumption, but we'll cross that bridge at the right time.  

**ncap@ncaplite.loc** This is the account to be used by the NCAP server.

###Connecting from the NCAP application.
Right now, I'm unable to create the SRV records that sleekXMPP looks
for in order to connect automatically, so we sill have to supply the
address,port tuple to the xmpp client, eg.

```
ugly_hardcoded_address=('10.10.100.4',5222)
xmpp.connect(ugly_hardcoded_address)
```

Python
======
The present version does not yet contain the python development environment.
Right now I'm just using this so I can spin up a local jabber server to
do some initial testing with. Once the framework is a bit more locked in
we'll add the python dev environment and a getting started tutorial for
other folks on the project.


I'm on Windows, please, God, help.
======
If anything comes up that requires a workaround on Windows boxes, we'll try to
document it here at first. Supposedly vagrant-hostmanager has support for Windows hosts as well, so maybe this section will
be pretty sparse after all :).

**Note 1:** You'll want to run all of this stuff from an elevated command prompt.
I'm assuming/hoping this is enough for the OS to let the scripts edit the hosts
file without a fuss.
