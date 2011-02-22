# Debconf configuration
sudo dpkg-reconfigure debconf
# set to dialog and low priority

# Installation of JVM by Oracle, do not use openjdk
# Added line to /etc/apt/sources.list
deb http://ppa.launchpad.net/sun-java-community-team/sun-java6/ubuntu lucid main

# Key activation for previous repository
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 3EBCE749

# Update
sudo apt-get update && sudo apt-get upgrade

# JRE installation
sudo apt-get install sun-java6-jre

# Ensure you are running the correct jre version
sudo update-alternatives --config java

# Download of ApacheDS deb file for your architecture
# use uname -a to known your arch
wget http://it.apache.contactlab.it//directory/apacheds/unstable/1.5/1.5.7/apacheds-1.5.7-amd64.deb

# Install Apache Directory Server
sudo dpkg -i apacheds-1.5.7-amd64.deb

# Configure your ApacheDS

# Corrected the running user of apacheds process to use privileded ports
# like 389 and 636 instead of 10389 and 10636 due to Plone issues.
vim /etc/init.d/apacheds-1.5.7-default

# change the line with RUN_AS_USER variable from
RUN_AS_USER=$APP_NAME
# to
RUN_AS_USER="root"

# Modify /var/lib/apacheds-1.5.7/default/conf/server.xml file

# Change the port and interfaces for process listening
# from
 <transports>
      <tcpTransport address="0.0.0.0" port="10389" nbThreads="8" backLog="50" enableSSL="false"/>
      <tcpTransport address="localhost" port="10636" enableSSL="true"/>
 </transports>

# to
 <transports>
      <tcpTransport address="0.0.0.0" port="389" nbThreads="8" backLog="50" enableSSL="false"/>
      <tcpTransport address="0.0.0.0" port="636" enableSSL="true"/>
 </transports>

# Add new partition
<partitions>
...
<jdbmPartition id="gem" cacheSize="1000" suffix="dc=gem,dc=org" optimizerEnabled="true"
                        syncOnWrite="true">

</partitions>


# Test your config launching
sudo /etc/init.d/apacheds-1.5.7-default console

# Ignore the errors: 
ERR_04450 The value {0}

# The istance is correctly running if you see
jvm 1    | Received a packet PING : ping
jvm 1    | Send a packet PING : ok
wrapperp | read a packet PING : ok


# Close apacheds with CTRL+C

# Start ApacheDS with normal script
sudo /etc/init.d/apacheds-1.5.7-default start

# Ensure the process is running
ps aux | grep apacheds

# You can see two process
# The first one for apacheds daemon
root     17699  0.0  0.1  17056   716 ?        Sl   09:35   0:00 /opt/apacheds-1.5.7/bin/apacheds /opt/apacheds-1.5.7/conf/apacheds.conf set.INSTANCE_HOME=/var/lib/apacheds-1.5.7 set.INSTANCE=default wrapper.syslog.ident=apacheds wrapper.pidfile=/var/run/apacheds-1.5.7/default.pid wrapper.daemonize=TRUE

# the second one for java container
root     17701  9.2 55.9 686908 212424 ?       Sl   09:35   0:10 java -Dlog4j.configuration=file:////var/lib/apacheds-1.5.7/default/conf/log4j.properties ...

# Simple firewall test with telnet
telnet localhost 389
telnet localhost 636

# Try the previous command from an external IP to your public IP
telnet 184.106.65.189 389
telnet 184.106.65.189 636

# Well done! Now, try to connect to your LDAP with an external client
BIND DN: uid=admin,ou=system
default password: secret

########################## REALLY IMPORTANT #############################
# Please, immediately change your password browsing uid=admin,ou=system #
# and changing userPassword attribute with sha encription               #
#########################################################################

# Add new ldif file to create the first dit and some example users, I use this example file:
# named init.ldif

version: 2

dn: dc=gem,dc=org
objectClass: dcObject
objectClass: organization
objectClass: top
dc: example
o: example.com
description: Creazione DIT

dn: ou=people,dc=gem,dc=org
objectClass: organizationalUnit
objectClass: top
ou: people

dn: cn=Test1,ou=people,dc=gem,dc=org
objectClass: person
objectClass: organizationalPerson
objectClass: inetOrgPerson
objectClass: top
cn: Test1
sn: Test1
mail: test1@redomino.com
uid: test1.test1
userPassword:: e1NIQX10RVNzQm1FL3lOWTNsYjZhMEw2dlZRRVpOcXc9

dn: cn=Test2,ou=people,dc=gem,dc=org
objectClass: person
objectClass: organizationalPerson
objectClass: inetOrgPerson
objectClass: top
cn: Test2
sn: Test2
mail: test2@redomino.com
uid: test2.test2
userPassword:: e1NIQX1FSjlMUEZEWHNOOXluU21ieHZqcDc1Qm1seDg9

dn: ou=aziende,dc=gem,dc=org
objectClass: organizationalUnit
objectClass: top
ou: aziende

dn: cn=Test1,ou=aziende,dc=gem,dc=org
objectClass: person
objectClass: organizationalPerson
objectClass: inetOrgPerson
objectClass: top
cn: Test1
sn: Test1
mail: test1@redomino.org
uid: test1.test1
userPassword:: e1NIQX10RVNzQm1FL3lOWTNsYjZhMEw2dlZRRVpOcXc9

dn: cn=Test2,ou=aziende,dc=gem,dc=org
objectClass: person
objectClass: organizationalPerson
objectClass: inetOrgPerson
objectClass: top
cn: Test2
sn: Test2
mail: test2@redomino.com
uid: test2.test2
userPassword:: e1NIQX1FSjlMUEZEWHNOOXluU21ieHZqcDc1Qm1seDg9

# Reload your entire DIT on the client and you should see users and units.
