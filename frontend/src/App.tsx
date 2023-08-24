import React, {useEffect} from 'react';
import './App.css';
import {Route, Routes} from "react-router-dom";
import Homepage from "./pages/Homepage";
import SecuredPage from "./pages/SecuredPage";
import Nav from "./components/Nav";
import ProtectedRoute from "./helpers/ProtectedRoute";
import {useKeycloak} from "@react-keycloak/web";
import {useAppDispatch} from "./store/store";
import {setCredentials} from "./store/users/usersSlice";

function App() {
    const {keycloak} = useKeycloak()
    const dispatch = useAppDispatch()

    useEffect(() => {
        if (keycloak.tokenParsed && keycloak.token) {
            dispatch(setCredentials({user: keycloak.tokenParsed.preferred_username, token: keycloak.token}))
        }
    }, [dispatch, keycloak.token, keycloak.tokenParsed]);

    return (
      <>
          <Nav/>
          <Routes>
              <Route path="/" element={<Homepage/>} />
              <Route path="/secured" element={
                  <ProtectedRoute>
                      <SecuredPage/>
                  </ProtectedRoute>
              } />
          </Routes>
      </>
  );
}

export default App;
