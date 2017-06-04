# OAuth Reverse Proxy

This Proxy could be placed in front of any website/webapp in order to add authentication via OAuth. It's based on the OAuth-Flask Python module which delivers default settings for gitlab and github as OAuth-Provider. Other providers could be added if the OAuth-endpoints are known. For more information see [https://github.com/swinkelhofer/oauth_flask]. The Reverse Proxy can be extended to inject logout-Buttons etc. into the website.

## Setup with Docker

 * Build the image: ```docker build -t oauth_reverse_proxy <PathToDockerfile>```
 * Run the container via docker-compose:
```docker
version: '2'
services:
  oauth-reverse-proxy:
    image: registry.zawiw.de:5000/swinkelhofer/oauth_reverse_proxy
    environment:
      OAUTH_CLIENT: xxxx
      OAUTH_SECRET: xyxy
      DOMAIN: example.com
      PROTOCOL: https
      OAUTH_PROVIDER: gitlab
      OAUTH_PROVIDER_URI: https://git.example.com
      UPSTREAM_HOSTNAME: my_service
      UPSTREAM_PORT: 9001
      REPLACE_CALLBACK: etherpad:inject_js
    links:
    - any_service:my_service

  any_service:
    # ...
```

## Configuration via Environment

Environment Variable | Explanation
-------------------- | -----------
OAUTH_CLIENT		 | OAuth Client Token. Get it via your OAuth Provider
OAUTH_SECRET		 | OAuth Secret for the Client Token
DOMAIN				 | Domain that should be secured via OAuth
PROTOCOL			 | Protocol of the Domain (Default http)
OAUTH_PROVIDER		 | Provider for the OAuth token (Default gitlab, github also possible. To add more, extend the oauth_flask module
OAUTH_PROVIDER_URI	 | URL of the OAuth Provider (in the shape http(s)://domain.tld)
UPSTREAM_HOSTNAME	 | The name (or IP) to reach the actual service that should be secured (e.g. another Container containing the webapp)
UPSTREAM_PORT		 | Port to reach the service that should be proxied
REPLACE_CALLBACK	 | If you provide an injection module (inject Logout-Button...) this variable tells which module and function should be called (shape: module:method)
