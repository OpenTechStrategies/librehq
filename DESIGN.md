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

For clear communication, we'll specify some terminology for services
and their sub-parts.  A given 'service' includes both an 'upstream
package' (e.g. MediaWiki), and a 'service wrapper', which is our
LibreHQ code for managing and working with the 'upstream package'.

Service wrapper code is written in Python (and JavaScript for
UI/front end), regardless of the language of the upstream package
(e.g. PHP).

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

## Service Modules

Each LibreHQ service is a Python module in its own directory. Some
conventions:

* The directory for the service will be just `<service>` (e.g. 'wikis')
* The service should use as a base `"/<service>/"` for web requests

### Service Templates

The template files for a service that are served by Flask are generated
by the Vue.js front end compile step. For example, a `wikis.html` file
is generated in `librehq/templates` where Flask looks for it. These
files are served by Flask as-is, without any data added to them, so
they're not really functioning as templates.  Rather, data is fetched
by a separate request to the server and added to the page by Vue.js.

### Outstanding questions

Some outstanding questions to be determined via development:

* Should service sections have their own look and feel that matches the
  service they provide, or should they adhere to a greater librehq
  design?
* What level of functionality should be exposed in the main dashboard
  through `main_partial`
* Currently submodules provide the UI/templates for their management,
  which are displayed within the main dashboard. Will they still do this
  when templating is moved to Vue.js? How? Would each submodule provide a
  Vue component that's rendered in the main dashboard? This would mean
  each submodule would have its own npm-managed front-end dependencies?

## Front End

[Vue.js](https://vuejs.org/) will be used on the front end for HTML
templating and for working with the DOM.  The Flask server will send
JSON data to be rendered into pages by Vue. One advantage of
this decoupled approach is it is easier to test the server in isolation
from the client, and vice-versa (by using mock JSON data). Further details
are TBD but one possibility would be to take a
['single-page-app'](https://en.wikipedia.org/wiki/Single-page_application)
approach.

From a user's perspective, the services that LibreHQ provides (wiki, chat,
etc.) will generally be separate from the LibreHQ UI. E.g. there will be a
LibreHQ UI for managing a wiki in the LibreHQ app, but when you visit the
wiki it will look like a regular vanilla wiki, and there won't be anything
Vue-rendered on the wiki pages, no LibreHQ header, footer, etc.

LibreHQ will use [npm](https://www.npmjs.com/) to manage Vue and other
front-end dependencies.

