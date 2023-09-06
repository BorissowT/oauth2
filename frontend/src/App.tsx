import React, {useEffect} from 'react';
import './App.css';
import {Route, Routes} from "react-router-dom";
import Homepage from "./pages/Homepage";
import SecuredPage from "./pages/SecuredPage";
import Nav from "./components/Nav";
import ProtectedRoute from "./helpers/ProtectedRoute";
import {useKeycloak} from "@react-keycloak/web";
import {useAppDispatch, useAppSelector} from "./store/store";
import {setCredentials} from "./store/users/usersSlice";

function App() {

    const {keycloak} = useKeycloak()
    const dispatch = useAppDispatch()

    const token = useAppSelector(state => state.user.token)

    useEffect(() => {
        if (keycloak.tokenParsed && keycloak.token) {
            dispatch(setCredentials({user: keycloak.tokenParsed.preferred_username, token: keycloak.token}))
        }
    }, [dispatch, keycloak, keycloak.token, keycloak.tokenParsed]);

    useEffect(() => {
        keycloak.onTokenExpired = () => {
            keycloak.updateToken(5).then((refreshed) => {
                if (refreshed) {
                    if (keycloak.token && keycloak.tokenParsed) {
                        dispatch(setCredentials({user: keycloak.tokenParsed.preferred_username,
                            token: keycloak.token}))
                    }
                }
            })
        }
    }, [dispatch, keycloak]);

    const getToken = () => {
        console.log(token)
    }

    return (
      <>
          <Nav/>
          <button onClick={getToken}>Get token</button>
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
