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

## Booting the appliaction

Start the application by running flask from the project directory:

```
$ FLASK_APP=librehq pipenv run flask run
```

## Using the application

At this time, the application runs locally on port 5000, so visit `http://localhost:5000` to view.
