# OAUTH 2
This is a test application. It demonstrates authorization code flow. Actors are react client app, authorization server (key cloak) and resource server (flask app).
<br/><br/>
## Roles<br/>
An OAuth 2.0 flow has the following roles:

### Resource Owner:<br/>
Entity that can grant access to a protected resource. Typically, this is the end-user.

### Resource Server:<br/> 
Server hosting the protected resources. This is the API you want to access.

### Client:<br/> 
Application requesting access to a protected resource on behalf of the Resource Owner.

### Authorization Server:<br/>
Server that authenticates the Resource Owner and issues access tokens after getting proper authorization. In this case, Auth0.
<br/> <br/>
to run a keycloak service:<br/>
docker-compose -f docker-compose-keycloak.yaml up -d
