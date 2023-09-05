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
<br/><br/>
## Terminology<br/>
<a href="https://www.keycloak.org/docs/latest/authorization_services/index.html#_overview_terminology" target="_blank">Documentation</a>
<br/><br/>
Before going further, it is important to understand these terms and concepts introduced by Keycloak Authorization Services.

### Resource
A resource is part of the assets of an application and the organization. It can be a set of one or more endpoints, a classic web resource such as an HTML page, and so on. In authorization policy terminology, a resource is the object being protected.

Every resource has a unique identifier that can represent a single resource or a set of resources. For instance, you can manage a Banking Account Resource that represents and defines a set of authorization policies for all banking accounts. But you can also have a different resource named Alice’s Banking Account, which represents a single resource owned by a single customer, which can have its own set of authorization policies.

### Scope
A resource’s scope is a bounded extent of access that is possible to perform on a resource. In authorization policy terminology, a scope is one of the potentially many verbs that can logically apply to a resource.

It usually indicates what can be done with a given resource. Example of scopes are view, edit, delete, and so on. However, scope can also be related to specific information provided by a resource. In this case, you can have a project resource and a cost scope, where the cost scope is used to define specific policies and permissions for users to access a project’s cost.

### Permission
Consider this simple and very common permission:

A permission associates the object being protected with the policies that must be evaluated to determine whether access is granted.

X CAN DO Y ON RESOURCE Z

where …​

X represents one or more users, roles, or groups, or a combination of them. You can also use claims and context here.

Y represents an action to be performed, for example, write, view, and so on.

Z represents a protected resource, for example, "/accounts".

Keycloak provides a rich platform for building a range of permission strategies ranging from simple to very complex, rule-based dynamic permissions. It provides flexibility and helps to:

Reduce code refactoring and permission management costs

Support a more flexible security model, helping you to easily adapt to changes in your security requirements

Make changes at runtime; applications are only concerned about the resources and scopes being protected and not how they are protected.

### Policy<br/>
A policy defines the conditions that must be satisfied to grant access to an object. Unlike permissions, you do not specify the object being protected but rather the conditions that must be satisfied for access to a given object (for example, resource, scope, or both). Policies are strongly related to the different access control mechanisms (ACMs) that you can use to protect your resources. With policies, you can implement strategies for attribute-based access control (ABAC), role-based access control (RBAC), context-based access control, or any combination of these.
Keycloak leverages the concept of policies and how you define them by providing the concept of aggregated policies, where you can build a "policy of policies" and still control the behavior of the evaluation. Instead of writing one large policy with all the conditions that must be satisfied for access to a given resource, the policies implementation in Keycloak Authorization Services follows the divide-and-conquer technique. That is, you can create individual policies, then reuse them with different permissions and build more complex policies by combining individual policies.
<br/><br/>
## 2.1.  Client Types (OAuth)
source: https://www.rfc-editor.org/rfc/rfc6749#section-2.1 <br/><br/>
   OAuth defines two client types, based on their ability to
   authenticate securely with the authorization server (i.e., ability to
   maintain the confidentiality of their client credentials):
<br/><br/>
   confidential<br/><br/>
      Clients capable of maintaining the confidentiality of their
      credentials (e.g., client implemented on a secure server with
      restricted access to the client credentials), or capable of secure
      client authentication using other means.
<br/><br/>
   public<br/><br/>
      Clients incapable of maintaining the confidentiality of their
      credentials (e.g., clients executing on the device used by the
      resource owner, such as an installed native application or a web
      browser-based application), and incapable of secure client
      authentication via any other means.
<br/><br/>
   The client type designation is based on the authorization server's
   definition of secure authentication and its acceptable exposure
   levels of client credentials.  The authorization server SHOULD NOT
   make assumptions about the client type.
<br/><br/>
   A client may be implemented as a distributed set of components, each
   with a different client type and security context (e.g., a
   distributed client with both a confidential server-based component
   and a public browser-based component).  If the authorization server
   does not provide support for such clients or does not provide
   guidance with regard to their registration, the client SHOULD
   register each component as a separate client.
<br/><br/>
### Usage of RPT token

The two invocations that you mention are not supposed to be by the same party.

The first one is authentication by the client app: it provides authent data (here, username + passwd) and gets a token from the authent service. This token can be used by the client app to access any service, provided the audience is ok, date is ok etc. The client does not know how any data or calls are protected, it just uses a token as a black box.

The service called, the resource server, acts as a policy enforcement point (PEP). It gets a token, validates it, and then uses it to enforce policies, refusing or granting access to this or that resource that it controls.
For this it needs to evaluate policies. That’s not its job, it’s the job of a Policy Decision Point (PDP), so it does the second call, to get permissions from the PDP. Here the PDP is Keycloak. The PEP calls it, saying hey I want to know if I can grant access to these particular resources with these particular claims (the JWT). Keycloak evaluates the policies against all this, acting as PDP, and returns the permissions in an RPT (which may be as simple as yes/no, by the way, it doesn’t need to be a JWT or even a list of resources).
(note that the PEP could simply look inside the JWT and check the claims instead of permissions, but that means you can’t manage policies any more, a whole different discussion)

 The<br/><br/>
curl -X POST   http://localhost:8080/auth/realms/${realm}/protocol/openid-connect/token  -H "Authorization: Bearer ${access_token}" --data "grant_type=urn:ietf:params:oauth:grant-type:uma-ticket" --data "audience={resource_server_client_id}"
<br/><br/>
#### useful links:

https://developers.redhat.com/blog/2020/01/29/api-login-and-jwt-token-generation-using-keycloak
<br><br>
https://www.youtube.com/watch?v=3K77Pvv-ouU
<br><br>
https://www.youtube.com/watch?v=M8ym5UwnnZg
<br><br>
docker run -p 8080:8080 -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin quay.io/keycloak/keycloak:latest start-dev --features=preview --http-relative-path=/auth
