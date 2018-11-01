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

Some users are individuals and some are organizations.  The two kinds
live in the same namespace (e.g., in URLs, they occupy the same
positions).  An organization user has a set of individual users as its
owners.  You can't log in as an organization; instead, to change
something about an organization, you would log in as a user who is an
owner of (or some level of admin for) that organization.

Note: There are other online services that work this way; we should
look at a few and compare, to make sure we're doing it right.

An individual can transfer assets (such as a wiki) to an organization,
and a forwarding pointer will optionally be left behind.  If she is
not an owner of the destination organization, someone there will have
to approve the transfer.

## Services and URLs

To create an account, start at `https://librehq.com/`.  Afterwards
you'll have a landing page at `https://USER.librehq.com/` that lists
all the services available and which ones are active (remember, in the
long run USER might be an organization rather than an individual).

Each active service has a subzone within that user's zone.  For
example, these are three distinct wikis:

* `https://wiki.USER-1.librehq.com/WIKINAME_1`
* `https://wiki.USER-1.librehq.com/WIKINAME_2`
* `https://wiki.USER-2.librehq.com/WIKINAME_1`

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

Some outstanding questions to be determined via development:

* Should service sections have their own look and feel that matches the
  service they provide, or should they adhere to a greater librehq
  design?
* What level of functionality should be exposed in the main dashboard
  through `main_partial`
