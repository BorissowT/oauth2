import Keycloak from "keycloak-js";
const keycloak = new Keycloak({
    url: "http://192.168.105.139:8080/auth",
    realm: "myrealm",
    clientId: "reactclient",
});

export default keycloak;