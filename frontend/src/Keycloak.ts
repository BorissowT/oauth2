import Keycloak from "keycloak-js";
const keycloak = new Keycloak({
    url: "http://192.168.105.139:8080/auth",
    realm: "Main",
    clientId: "react-auth1",
});

export default keycloak;