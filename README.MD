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

### Policy
A policy defines the conditions that must be satisfied to grant access to an object. Unlike permissions, you do not specify the object being protected but rather the conditions that must be satisfied for access to a given object (for example, resource, scope, or both). Policies are strongly related to the different access control mechanisms (ACMs) that you can use to protect your resources. With policies, you can implement strategies for attribute-based access control (ABAC), role-based access control (RBAC), context-based access control, or any combination of these.
Keycloak leverages the concept of policies and how you define them by providing the concept of aggregated policies, where you can build a "policy of policies" and still control the behavior of the evaluation. Instead of writing one large policy with all the conditions that must be satisfied for access to a given resource, the policies implementation in Keycloak Authorization Services follows the divide-and-conquer technique. That is, you can create individual policies, then reuse them with different permissions and build more complex policies by combining individual policies.

