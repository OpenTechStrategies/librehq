# LibreHQ

This is a placeholder description that should be filled out.

## Services

LibreHQ offers various services that are organized as separate Python
modules and use separate databases. Currently these are:

* wikis: a wiki hosting and generation tool

# Installing

LibreHQ uses ansible to install.  Please see INSTALL.md in the ansible
directory.

# Running

LibreHQ uses [`pipenv`](https://docs.pipenv.org/) to manage its back end
dependencies and handle running the server.

```ShellSession
$ FLASK_APP=librehq pipenv run flask run
```

## Starting a mock mail server

LibreHQ sends out email to port 1025 for certain actions, which can be listened to
using a standalone python invocation:

```ShellSession
$ python -m smtpd -n -c DebuggingServer localhost:1025
```

This is required in order to use certain parts of the site, and not having it
running may result in errors.

## Using the application

Part of the ansible setup is to install apache files with port forwarding.
While you can probably access the application via `http://localhost:5000`,
make sure to test by using `http://__YOUR_LIBREHQ_HOSTNAME__`.

The reason for this is that the other services not part of core librehq will
use that address, meaning it's useful error prevention to ensure that it's
all set up and working correctly.

## Test csv2wiki data

There are files in testdata that you can use to populate a wiki using the
csv2wiki tool via the interface (Populate wiki with csv data).

# Extra tasks

If you have installed from ansible, and are just using the app without
development, you can stop here.

For developers that may need to update the database, regenerate the html/js
files, and do active work on the site, more information and useful commands
follow.

## Back End: Running migrations

While the ansible playbook will take care of running the migrations, you may
need to run them manually at times, and can do so with:

```ShellSession
FLASK_APP=librehq pipenv run flask db upgrade
```

## Front End: Dependencies

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

With this setup, going to \<servername\>/client/wikis.html will load the wiki data
from the python server, allowing you to dynamically test your frontend code and
backend code simultaneously
