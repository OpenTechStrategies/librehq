# LibreHQ

This is a placeholder description that should be filled out.

# Running

## Dependencies

LibreHQ uses [`pipenv`](https://docs.pipenv.org/) to manage its dependencies.
There are various installation instructions in the documentation but the common
ones are:

* Using pip: `pip install pipenv`
* Using brew: `brew install pipenv`

Then run `pipenv` to get all the local dependencies (see the Pipfile for the
full list)

```
$ pipenv install

# Initialize pipenv for submodules, which is needed for database migrations later.
$ for submodule in wikis ; do
  (cd $submodule ; pipenv install)
done
```

### Sub modules

Each section of librehq is setup as its own project, which should be bootable
independently for development and testing, which is then added as a submodule
to this project.  Currently added are:

* librehq-wikis as wikis: a wiki hosting and generation tool

## Setting up the apps configuration

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

## Configuring the database

LibreHQ uses [flask-migrate](https://flask-migrate.readthedocs.io/en/latest/),
[SQLAlchemy](https://www.sqlalchemy.org/), and
[Alembic](https://alembic.zzzcomputing.com/en/latest/)  to manage migrations
and the database.  Mostly this is done by just updating the model and running
`FLASK_APP=librehq pipenv run flask db migrate` to create the revisions.

Create a user and database for the application.  For now, the user/password
is harcoded in the application, and so needs to match the following:

```ShellSession
$ sudo -u postgres createuser librehq
$ sudo -u postgres createdb --owner=librehq librehq_core
$ sudo -u postgres createdb --owner=librehq librehq_wikis # For wikis submodule
```

Run flask-migrate migrations
```ShellSession
FLASK_APP=librehq pipenv run flask db upgrade
```

Then run migrate for each of the submodules.  The reason we do it this way is
so that each submodule can handle their own database setup, and leave core to
be nothing more than a submodule collector.  Each submodule also needs its own
config.py that has the default database matching the submodule database (they
should each have a .tmpl to use)

```ShellSession
for submodule in wikis ; do
  (cd $submodule ; FLASK_APP=$submodule pipenv run flask db upgrade)
done
```

**NOTE:** If you want to use `flask db migrate`, you need to disable importing
of the submodules or else you'll get automatic generate of revisions for those
submodules.  If this becomes a hassle, then in the future some kind of top level
swtich should be used.

## Starting a mock mail server

LibreHQ sends out email to port 1025 for certain actions, which can be listened to
using a standalone python invocation:

```ShellSession
$ python -m smtpd -n -c DebuggingServer localhost:1025
```

This is required in order to use certain parts of the site, and not having it
running may result in errors.

## Booting the appliaction

Start the application by running flask from the project directory:

```
$ FLASK_APP=librehq pipenv run flask run
```

## Using the application

At this time, the application runs locally on port 5000, so visit `http://localhost:5000` to view.
