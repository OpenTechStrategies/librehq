# The Design of LibreHQ

WIP / comments welcome; this is all tentative.

## Authentication, Identities, and Usernames

User identity is shared across all LibreHQ services.  LibreHQ will
provide a core authentication mechanism.  As much as possible, the
same display name and/or username are used across all services.  For
example, if you are user `PatMendoza` in the wiki with "Pat Mendoza"
as your display name, you will also show with that identity in the
chat service, the feedreader service, the collaborative document
service, etc.

(Right now we don't think any of the upstream tools we will package
require usernames that look like email addresses; if they do, we'll
cross that bridge when we come to it.)

## Individuals and Organizations

_(Note: the "individual" part of this will be implemented first, and
the "organization" part will come later.)_

Some users are individuals and some are organizations.  The two kinds
live in the same namespace (e.g., in URLs, they occupy the same
positions).  An organization user has a set of individual users as its
owners.  You can't log in as an organization; instead, to change
something about an organization, you would log in as a user who is an
owner of (or some level of admin for) that organization.

_(Note: There are other online services that work this way; we should
look at a few and compare, to make sure we're doing it right.)_

An individual can transfer assets (such as a wiki) to an organization,
and a forwarding pointer will optionally be left behind.  If she is
not an owner of the destination organization, someone there will have
to approve the transfer.

## Services and URLs

To create an account, start at `https://librehq.com/`.  Afterwards
you'll have a landing page at `https://librehq.com/USER` that lists
all the services available and which ones are active (remember, in the
long run USER might be an organization rather than an individual).

Each active service has a subzone within that user's zone.  For
example, these are three distinct wikis:

* `https://librehq.com/USER_1/wiki/WIKINAME_1`
* `https://librehq.com/USER_1/wiki/WIKINAME_2`
* `https://librehq.com/USER_2/wiki/WIKINAME_1`

As a general rule, every component of a URL should be meaningful,
human-readable, and (when it's under our control) short.  We can't do
anything about the "https://" part, but we can try to adhere to this
principle everywhere else.

_Question: Does the above URL and path scheme affect our ability to
shard load across servers?  I'm presuming not, since many sites work
this way._

Internally, we use a random token as the user's single, unique
cross-service account identifier.  We don't use any of the
externally-visible tokens (such as the username) for this; that way if
someone wants to change their username, we have the option to allow
it.  We'd have to decide what our policy is on that -- e.g., do we
forward from the old username for up to some predetermined amount of
time -- but at least we can set things up so that this is a policy
decision rather than a technical constraint.

## Modules

Each LibreHQ service gets its own repository, in order to keep the
development lifecycle of each codebase separate.  They are imported
into LibreHQ-core via git submodules, and expose their functionality
through partials and flask blueprints.  Some conventions:

* The repository name is `librehq-<service>`, with the directory for
  the git submodule to be just `<service>`
* Only merge submodule sha changes to librehq-core when stable, and
  collapse so that only one sha update is done
* Submodule sha updates should live in their own commits
* The service should be bootable on its own, via flask
* The service should expose a `from service import bp` which represents
  the Blueprint for that submodule
* The Blueprint should use as a base `"/<service>/"` for web requets
* The service should expose a `main_partial()` that returns a template
  to be imported into the main section

### Templates

When designing module pages, all of the templates should be in the
`templates/<modulename>/` subdirectory to prevent confusion in the top
level directory.  For instance, if you have `templates/dashboard.html`,
in your module, when running as part of the larger librehq site, the main
core `templates/dashboard.html` will get chosen for rendering, even if
called from the module Blueprint.  So, you need to have (for example)
`templates/wikis/dashboard.html` and reference `wikis/dashboard.html` in
your modules flask code.

Similarly, you should include the line:

```
{% if not g.standalone %}{% extends "base.html" %}{% endif %}
```

in all of your templates to pull in the header/footer from the core package
when not running as a standalone app.  Then, in your standalone bootup
section (usually in `__init__.py`), you should have the following:

```python
@app.before_request
def set_standalone():
    g.standalone = True
```

### Third Party Libraries

JS and CSS third party libraries loaded by the LibreHQ app should be served
from our servers, rather than from elsewhere like a CDN (Content Delivery
Network). The versions of these libraries that we use should be committed
and tracked by git. The reasons for this include consistency and security.

For minified versions of these libraries (i.e. bulma.css and bulma.min.css),
both versions should be present in the repo and also on our servers, so that
anyone can just remove the 'min' from the URL to see the non-minified
source code.

### Outstanding questions

Some outstanding questions to be determined via development:

* Should service sections have their own look and feel that matches the
  service they provide, or should they adhere to a greater librehq
  design?
* What level of functionality should be exposed in the main dashboard
  through `main_partial`
