# CONTRIBUTING

## Git Branches

In addition to short-lived 'feature' branches where work on particular
issues is done, there will be several long-lived git branches for
various purposes. Basically changes will work their way from the top of
this list to the bottom.

- __mvp-dev__: Contains work in progress on the initial 'minimum viable
product'. Feature branches are merged into this branch during this
initial mvp phase. In this early phase, the level of review for merging
code into this branch need not be as high as for merging to master.
This branch will go away after the mvp phase.
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
