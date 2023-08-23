import {FC, ReactElement} from 'react';
import {useKeycloak} from "@react-keycloak/web";

interface ProtectedRouteProps {
    children: ReactElement
}

const ProtectedRoute: FC<ProtectedRouteProps> = ({children}) => {
    const { keycloak } = useKeycloak();

    const isLoggedIn = keycloak.authenticated;


    return isLoggedIn ? children : null;
};

export default ProtectedRoute;