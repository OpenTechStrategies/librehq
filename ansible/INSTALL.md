# Installing LibreHQ

Installation is done using ansible.  While you can execute these instructions as
a developer, the best way is to use ansible so we continue to keep the playbooks
up to date.  For that reason, when adding something to the installation, instead
add it to the correct role and so that other developers can just re-run and pull
your changes.

# Setting up your system

## Installing ansible

You can most likely just use the ansible provided by your distro:

```ShellSession
 $ sudo apt-get install ansible
```

## Setting up your hosts file

The easiest way to create a local ansible hosts file, by using one of the templates
in the current directory.  You can make this global by copying to `/etc/ansible/hosts`

```
$ cp hosts.localhost.tmpl hosts
```

or, if you'd prefer to use a different machine / user:
```
$ cp hosts.remote.tmpl hosts
$ edit hosts
```

You'll see two groups, one for mediawiki and one for LibreHQ.  This is so you
can provision the two parts of the system on different machines if you like.

You may have as many hosts as you like within the groups.  You should have
SSH access to those hosts with your current user, either via keys or ssh-agent.
You can test the connection to them with `ansible -i hosts mediawiki -m ping`.
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

## Setting up the mediawiki hosts file

When adding, removing, or renaming a wiki, librehq runs ansible scripts.  This
requires the user running librehq to be able to execute ssh commands on the
machine running mediawiki, as well as to be properly configured.

```ShellSesssion
 $ cp roles/librehq/files/mwiki-hosts.tmpl roles/mediawiki/files/mwiki-hosts
 # Edit roles/mediawiki/files/mwiki-hosts
```

# Running the playbook

The one liner to run the playbook:

```ShellSesssion
 $ ansible-playbook -i hosts all.yml
```

# Starting the services

Refer to the README.md in the project root for starting all the services
once installed.

# Useful tools for running in development

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

# Using Vagrant

If you would like to use vagrant to quickly boot up a version,
it's straightforward with a few additional steps.

First, set up your variables as documented above.

Then, get vagrant:

    $ sudo apt-get install vagrant
    $ sudo apt-get install virtualbox

Note that the [Vagrant
documentation](https://www.vagrantup.com/docs/installation/) suggests
_not_ using the version of Vagrant packaged by your operating system,
but rather using the more complete and up-to-date versions they
[provide](https://www.vagrantup.com/downloads.html).

(2018/12/06: the version from the Vagrant website worked (2.2.2),
but the one provided by Ubuntu 18.04 did not (2.0.2).)

Either way, downloading may take a few minutes.  If you choose to
download the `.deb` file, you can install it with `sudo dpkg -i
/path/to/vagrant_2.2.1_x86_64.deb`.  Once installed, you can enter into
the vagrant directory and run:

    $ vagrant up

You may get a persistent error like `default: Warning: Authentication
failure. Retrying...`.  Check that the virtual machine is being created
correctly in VirtualBox (you can look in the GUI to see if it appears
and is running).  The quickest and simplest way to resolve this is by
copying [the Vagrant default key
files](https://github.com/hashicorp/vagrant/tree/master/keys) to your
`.ssh` directory (on your host machine, not the new virtual guest
machine).  The Vagrantfile assumes that this default private key is
present at `~/.ssh/vagrant-insecure`, as noted in the line
`config.ssh.private_key_path = "~/.ssh/vagrant-insecure"`. Make sure
the default key files end in a newline (see this [bug
report](https://github.com/hashicorp/vagrant/issues/10333)).

If you need to test a clean build, you can clear the Vagrant virtual
machine with `vagrant destroy`.  From there, just start again at
`vagrant up` above.

If all goes well, you'll see the two ansible scripts execute.

## Additional needed steps

In order to seamlessly use the vagrant server with on your local
machine, there are three additional steps you need.

### dnsmasq

Firstly, you need to get a dnsserver running, easiest way is to
follow the steps above in the dnsmasq section.  You'll need to
have your local dns wildcard to your local machine as explained
above.

### Host Apache config

Secondly, you need to ProxyPass apache for the dns server name
you have to port 8080 using a configuration like the following:

```
<VirtualHost __SERVER_NAME__:80>

  ServerName __SERVER_NAME__
  ServerAlias *.__SERVER_NAME__

  ProxyPreserveHost On
  ProxyPass / http://127.0.0.1:8080/
  ProxyPassReverse / http://127.0.0.1:8080/

</VirtualHost>
```

The reason this is needed is because, for right now, mediawikifarm
doesn't play well with ports being in the url name.  Not too much
effort was gone into to figure out exactly why, but 500 errors were
coming out.

### Vagrant ansible hosts file

In order to install wikis, ansible inside vagrant needs to find
itself when looking for the [mediawiki] group.  The easiest way
is to `vagrant ssh` when in the vagrant directory, and then
add the following lines to /etc/ansible/hosts:

```
[mediawiki]
localhost ansible_connection=local
```

## Checking LibreHQ in the browser

When all is done, you should be able to load up `http://__SERVER_NAME__/`
in your browser to see the interface

## Looking at logs

Two logfiles are created from the services running, flask.log and mailer.log,
that can be viewed after using `vagrant ssh` to get into the box.  The latter
is needed for the verification links.

## Keeping vagrant up to date

The easiest way to keep your vagrant server up to date is to reprovision it
with `vagrant provision` after bringing your local checkout up to date with
master (to get any new ansible tasks).
