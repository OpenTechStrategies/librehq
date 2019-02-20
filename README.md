# LibreHQ

This is a placeholder description that should be filled out.

## Services

LibreHQ offers various services that are organized as separate Python
modules and use separate databases. Currently these are:

* wikis: a wiki hosting and generation tool

# Running

## Back End: Dependencies

LibreHQ uses [`pipenv`](https://docs.pipenv.org/) to manage its back end
dependencies. There are various installation instructions in the documentation
but the common ones are:

* Using pip: `pip install pipenv`
* Using brew: `brew install pipenv`

Then run `pipenv` to get all the local dependencies (see the Pipfile for the
full list)

```ShellSession
$ pipenv install --python 3.6 --dev
```


## Back End: Setting up the app's configuration

The application will try to load the configuration from config.py in the core
directory, and then after from a file noted by `LIBREHQ_CONFIG`.  This means that
you can use a default config in the main directory and override if you choose.

A `config.py.tmpl` has been provided with all the variables that the application
needs to run.

### Using config.py

You can copy the `config.py.tmpl` to `config.py` and update it with your system's
configuration, such as database information.

### Using the LIBREHQ_CONFIG environment variable

Alternately, you can place a file to be loaded up somewhere and refer to it
by the absolute path.  When starting up, you'll modify the flask commands as
follows:

```ShellSession
$ FLASK_APP=librehq LIBREHQ_CONFIG=/path/to/myconfig.py pipenv run flask run
```

## Back End: Configuring the databases

LibreHQ uses [flask-migrate](https://flask-migrate.readthedocs.io/en/latest/),
[SQLAlchemy](https://www.sqlalchemy.org/), and
[Alembic](https://alembic.zzzcomputing.com/en/latest/)  to manage migrations
and the databases.  Mostly this is done by just updating the model and running
`FLASK_APP=librehq pipenv run flask db migrate` to create the revisions.

Create a database user and databases owned by that user. You will be prompted
to enter/create a password for the database user. Make a note of this password.
For now, the user name is harcoded in the application, and so needs to match
the following:

```ShellSession
$ sudo -u postgres createuser --pwprompt librehq
$ sudo -u postgres createdb --owner=librehq librehq_core
$ sudo -u postgres createdb --owner=librehq librehq_wikis # For wikis service 
```

Run flask-migrate migrations
```ShellSession
FLASK_APP=librehq pipenv run flask db upgrade
```

## Front End: Dependencies

LibreHQ uses [npm](https://www.npmjs.com/package/npm) to manage front end
dependencies such as [Vue.js](https://vuejs.org/). The easy and recommended way
to install npm, is to install [node](https://nodejs.org/en/), which comes with
npm.

Once you have npm installed, move to the `client` directory.

```ShellSession
$ cd client
```

Dependencies are specified in the package.json and package-lock.json files.
Install these dependencies like so:

```ShellSession
$ npm install
```

Not required for a minimal install, but doing a global (`-g`) install of the
[Vue command line tool](https://cli.vuejs.org) may be useful for front end
development:

```ShellSession
$ npm install -g @vue/cli
```

## Front End: Compilation Steps

Now run the "compile and minify for production" command:

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

## Starting a mock mail server

LibreHQ sends out email to port 1025 for certain actions, which can be listened to
using a standalone python invocation:

```ShellSession
$ python -m smtpd -n -c DebuggingServer localhost:1025
```

This is required in order to use certain parts of the site, and not having it
running may result in errors.

## Backend: Setting up mediawiki

Mediawiki and MediawikiFarm are set up via the wikis subproject.  Read
wikis/ansible/README.md to set up.  You will need to ensure that the wikis
created in that farm are accessible via \<wiki\_name\>.\<WIKI\_URL\> (which
is set up in the config.py)

## Booting the application

Start the application by running flask from the project directory:

```
$ FLASK_APP=librehq pipenv run flask run
```

## Using the application

At this time, the application runs locally on port 5000, so visit `http://localhost:5000` to view.
