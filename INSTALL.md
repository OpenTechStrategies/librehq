# Installing LibreHQ

We cover three installation scenarios:

* You want to quickly try out LibreHQ -- "kick the tires", so to speak.
  For this, we recommend the [Vagrant deployment](#vagrant-deployment).

* You're a developer and want to set up an instance of LibreHQ that
  you might then proceed to hack on.  For this, we recommend the
  [dev deployment](#development-deployment).

* You're deploying a live instance of LibreHQ, for production or maybe
  for pre-production testing.  For this, we recommend the
  [production-deployment](#production-deployment).

In the first two of these cases, there's some custom DNS setup you
need to do, covered below in [DNS setup](#dns-setup).  In the dev
setup case, there's also some Apache proxying setup, covered

## DNS setup

This is needed for both Vagrant and dev deployment.  If you're doing a
production deployment, Presumably you have already set up a public DNS
server to respond to name requests in the necessary way.

DNS name resolution matters in LibreHQ because of the way LibreHQ
expects certain algorithmically-determined service names to exist
(e.g., wiki instances within the MediaWiki farm).  So even if you're
running a development or test instance entirely on localhost, you'll
still need to be able to DNS-resolve those names (e.g.,
`http://testuser.wiki.localhost`).

Instead of trying to anticipate every such name and hardcode a
corresponding mapping line into `/etc/hosts`, we recommend that you
set up the lightweight `dnsmasq` server:

    $ sudo apt-get install dnsmasq
    $ sudo ${EDITOR} /etc/resolv.conf
    ### Add a line "nameserver localhost" in first position,
    ### so it takes precedence over any remote nameservers.
    $ sudo ${EDITOR} /etc/dnsmasq.conf
    ### Add a line "address=/.wiki.localdomain.tld/127.0.0.1",
    ### which will enable LibreHQ to find the MediaWiki farm.

## Apache HTTPD config

This is only needed for dev deployment; you can skip it if you're
doing Vagrant or production deployment.

Apache will need to proxy any URLs that contain the 8080 port number.
This is because mediawikifarm doesn't play well with URLs that have
port numbers; we haven't spent too much effort figuring out exactly
why yet, but we were getting 500-class errors and this seemed to solve
it.  So put something like the below in your Apache configuration (on
Debian, that's probably in `/etc/apache2/conf-available/librehq.conf`
or something like that, but the exact path may be different for you):

    <VirtualHost __SERVER_NAME__:80>
    
      ServerName __SERVER_NAME__
      ServerAlias *.__SERVER_NAME__
    
      ProxyPreserveHost On
      ProxyPass / http://127.0.0.1:8080/
      ProxyPassReverse / http://127.0.0.1:8080/
    
    </VirtualHost>

## Vagrant deployment

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

### Vagrant ansible hosts file

In order to install wikis, ansible inside vagrant needs to find
itself when looking for the [mediawiki] group.  The easiest way
is to `vagrant ssh` when in the vagrant directory, and then
add the following lines to `/etc/ansible/hosts`:

```
[mediawiki]
localhost ansible_connection=local
```

### Keeping vagrant up to date

The easiest way to keep your vagrant server up to date is to reprovision it
with `vagrant provision` after bringing your local checkout up to date with
master (to get any new ansible tasks).

## Development deployment

Development deployment is mostly done through ansible, but remember
you must have taken care of the [DNS](#DNS-setup)
and [Apache proxying](#apache-httpd-config) prerequisites first.

While you could execute these instructions manually, the best way is
to use ansible, so that we can keep the playbooks up to date.  If you
add a new step, please do so by updating the appropriate ansible role,
so that other developers can just pull your changes and re-run.

### Installing ansible

You can most likely just use the ansible provided by your distro:

```ShellSession
 $ sudo apt-get install ansible
```

### Setting up your hosts file

The easiest way to create a local ansible hosts file, by using one of the templates
in the current directory.  You can make this global by copying to `/etc/ansible/hosts`

```ShellSesssion
$ cp hosts.localhost.tmpl hosts
```

or, if you'd prefer to use a different machine / user:
```ShellSesssion
$ cp hosts.remote.tmpl hosts
$ edit hosts
```

You'll see two groups, one for mediawiki and one for LibreHQ.  This is
so you could provision the two parts of the system on different
machines if you wanted to.

You may have as many hosts as you like within the groups.  You should have
SSH access to those hosts with your current user, either via keys or ssh-agent.
You can test the connection to them with `ansible -i hosts mediawiki -m ping`.
You should see something like the following for each host in your `[mediawiki]`
group:

```ShellSesssion
example.com | SUCCESS => {
    "changed": false, 
    "ping": "pong"
}
```

You also need to have sudo access for those users.  You can either
update the `/etc/sudoers` file to not need a password, or add the
`--ask-become-pass` option when running the `ansible-playbook`
command.

### Setting up needed variables

All the configurable variables for LibreHQ live in `group_vars/all`, and you can
generate that file via:

```ShellSesssion
 $ cp group_vars/all.tmpl group_vars/all
```

Look in that file for information about the variables and how you can set them

#### Note about secrets

While ansible does have the ability to encrypt secrets so they can be checked in
and unlocked when running, librehq uses ansible to act on other servers and
doesn't have the ability to unlock vaults, and the design decisions around that
have not been made.  For now, while running in prototype mode, secrets stay
unlocked.

### Setting up the mediawiki hosts file

When adding, removing, or renaming a wiki, librehq runs ansible scripts.  This
requires the user running librehq to be able to execute ssh commands on the
machine running mediawiki, as well as to be properly configured.

```ShellSesssion
 $ cp roles/librehq/files/mwiki-hosts.tmpl roles/mediawiki/files/mwiki-hosts
 # Edit roles/mediawiki/files/mwiki-hosts
```

### Running the playbook

```ShellSesssion
 $ ansible-playbook -i hosts all.yml
```

## Starting a mock mail server

LibreHQ sends out email to port 1025 for certain actions, which can be listened to
using a standalone python invocation:

```ShellSession
$ python -m smtpd -n -c DebuggingServer localhost:1025
```

This is required in order to use certain parts of the site, and not having it
running may result in errors.

## Running

LibreHQ uses [`pipenv`](https://docs.pipenv.org/) to manage its back end
dependencies and handle running the server.

```ShellSession
$ FLASK_APP=librehq pipenv run flask run
```

Part of the ansible setup is to install apache files with port forwarding.
While you can probably access the application via `http://localhost:5000`,
make sure to test by using `http://__YOUR_LIBREHQ_HOSTNAME__`.

The reason for this is that the other services not part of core librehq will
use that address, meaning it's useful error prevention to ensure that it's
all set up and working correctly.

## Checking LibreHQ in the browser

When all is done, you should be able to load up `http://__SERVER_NAME__/`
in your browser to see the interface

## Looking at logs

Two logfiles are created from the services running, flask.log and mailer.log,
that can be viewed after using `vagrant ssh` to get into the box.  The latter
is needed for the verification links.

## Extra tasks

If you have installed from ansible, and are just using the app without
development, you can stop here.

For developers that may need to update the database, regenerate the html/js
files, and do active work on the site, more information and useful commands
follow.

### Back End: Running migrations

While the ansible playbook will take care of running the migrations, you may
need to run them manually at times, and can do so with:

```ShellSession
FLASK_APP=librehq pipenv run flask db upgrade
```

### Front End: Dependencies

LibreHQ uses [npm](https://www.npmjs.com/package/npm) to manage front end
dependencies such as [Vue.js](https://vuejs.org/).  While the playbook will
handle installation of everything, you will need to regenerate the client
at times as you work:

```ShellSession
$ npm run build
```

This command generates HTML, JavaScript, and CSS files for each page, and puts
them where Flask can find them. So it needs to be done before booting the
application (described below).

For front end development that doesn't involve the back end, you can also just
do the "compile and hot-reload for development" command:

```ShellSession
$ npm run serve
```

Then point your browser to URLs that include the `.html` extension, like
`http://localhost:8080/client/dashboard.html`.  We use "/client/" here to allow
you to run both the npm server, and the python server simultaneously and via
a proxy pass configuration like the following, use them together:

```
  ProxyPass /client/ http://127.0.0.1:8080/client/
  ProxyPassReverse /client/ http://127.0.0.1:8080/client/
  ProxyPass / http://127.0.0.1:5000/
  ProxyPassReverse / http://127.0.0.1:5000/
```

With this setup, going to `\<servername\>/client/wikis.html` will load the wiki data
from the python server, allowing you to dynamically test your frontend code and
backend code simultaneously
