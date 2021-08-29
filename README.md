# FreshAir

A cobbled together solution to run moderate twitter content during follower interactions. <br />
To install, run install.ps1 as admin <br />
To run, use start.bat, and go to http://127.0.0.1:8080 <br />
<br />
- __Pros__:
  - Doesn't require a backend database
  - Doesn't require a Twitter developer account
- __Cons__:
  - No backend database (Can get slow during very high volumes)
  - No direct API access means doing things the round-about way, meaning slower tweet discovery, and potentially having stuff fall through the cracks
