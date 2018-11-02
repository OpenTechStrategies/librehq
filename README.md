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
```

### Sub modules

Each section of librehq is setup as its own project, which should be bootable
independently for development and testing, which is then added as a submodule
to this project.  Currently added are:

* librehq-wikis as wikis: a wiki hosting and generation tool

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
```

Run flask-migrate migrations
```ShellSession
FLASK_APP=librehq pipenv run flask db upgrade
```

## Booting the appliaction

Start the application by running flask from the project directory:

```
$ FLASK_APP=librehq pipenv run flask run
```

## Using the application

At this time, the application runs locally on port 5000, so visit `http://localhost:5000` to view.
