# CONTRIBUTING

## Git Branches

In addition to short-lived 'feature' branches where work on particular
issues is done, there will be several long-lived git branches for
various purposes. Basically changes will work their way from the top of
this list to the bottom.

- __master__: All feature branches merged into master are tested and
reviewed via pull requests on github before being merged in.
- __testing__ and/or __demo__: Code that is loaded on testing and/or
demo servers. May have changes/features that aren't in production yet.
- __production__: The stable code that is 'officially released' for use
in production installations/servers.

## Third Party Libraries

JS and CSS third party libraries loaded by the LibreHQ app should be served
from our servers, rather than from elsewhere like a CDN (Content Delivery
Network). The versions of these libraries that we use should be committed
and tracked by git. The reasons for this include consistency and security.
