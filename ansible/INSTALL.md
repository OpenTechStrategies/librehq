# Installing LibreHQ

Installation is done using ansible.  While you can execute these instructions as
a developer, the best way is to use ansible so we continue to keep the playbooks
up to date.  For that reason, when adding something to the installation, instead
add it to the correct role and so that other developers can just re-run and pull
your changes.

# Setting up your system

## Setting up your hosts file

The easiest way to set up the hosts file is by modifying `/etc/ansible/hosts`
You'll need two groups, one for mediawiki and one for LibreHQ.  This is so you
can provision the two parts of the system on different machines if you like.

You may have as many hosts as you like within the groups.  You should have
SSH access to those hosts with your current user, either via keys or ssh-agent.
You can test the connection to them with `ansible mediawiki -u root -m ping`.
You should see something like the following for each host in your `[mediawiki]`
group:

```
example.com | SUCCESS => {
    "changed": false, 
    "ping": "pong"
}
```

You also need to have sudo access for those users.  You can either update the
sudoers file to not need a password, or use `--ask-become-pass` when running the
ansible-playbook command.

### Sample hosts file for localhost

This a simple hosts file that you can install in `/etc/ansible/hosts` to install
the entire LibreHQ locally, using the current user:

```
[mediawiki]
localhost

[librehq]
localhost
```

### Sample hosts file for different user on different machines

```
[mediawiki]
wiki.librehq.com
remote_user=<username>

[librehq]
librehq.com
remote_user=<username>
```

## Setting up needed variables

All the configurable variables for LibreHQ live in `group_vars/all`, and you can
generate that file via:

```ShellSesssion
 $ cp group_vars/all.tmpl group_vars/all
```

Look in that file for information about the variables and how you can set them

### Note about secrets

While ansible does have the ability to encrypt secrets so they can be checked in
and unlocked when running, librehq uses ansible to act on other servers and
doesn't have the ability to unlock vaults, and the design decisions around that
have not been made.  For now, while running in prototype mode, secrets stay
unlocked.

# Running the playbook

The one liner to run the playbook:

```ShellSesssion
 $ ansible-playbook all.yml
```

# Useful tools for running in development

## Apache

By default, mediawiki has some changes to the apache the farm is installed on,
but librehq can just be accessed via localhost:5000.  However, if you want to
host somewhere else and not open up that port to the world, the following apache
site config can be useful:

```
<VirtualHost *:80>
  ProxyPreserveHost On
  ProxyPass /client/ http://127.0.0.1:8080/client/
  ProxyPassReverse /client/ http://127.0.0.1:8080/client/
  ProxyPass / http://127.0.0.1:5000/
  ProxyPassReverse / http://127.0.0.1:5000/
  ServerName __YOUR_SERVER_NAME_HERE__
</VirtualHost>
```

## dnsmasq

When running locally, in order to use csv2wiki and mediawikifarm,
the hostname you run under needs to support wildcard dnses.  The
reason is that mediawikifarm requires domains that look like
`http://test.wiki.domain.tld` in order to route.  A useful dns
server is dnsmasq.  After installing it, and adding localhost
to your resolv.conf, adding the following line to /etc/dnsmasq.conf
will make it so librehq can find the farm, and apache will pass
along requests correctly:

```
address=/.wiki.localdomain.tld/127.0.0.1
```
