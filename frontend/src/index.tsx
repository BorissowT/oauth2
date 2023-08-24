import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import {BrowserRouter, Route, Routes} from "react-router-dom";
import {Provider} from "react-redux";
import {store} from "./store/store";
import {ReactKeycloakProvider} from "@react-keycloak/web";
import keycloak from "./Keycloak";

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  <Provider store={store}>
      <ReactKeycloakProvider authClient={keycloak}>
          <BrowserRouter>
              <Routes>
                  <Route path={"/*"} element={<App/>}/>
              </Routes>
          </BrowserRouter>
      </ReactKeycloakProvider>
  </Provider>
);
