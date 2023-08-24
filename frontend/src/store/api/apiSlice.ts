import {BaseQueryApi, createApi, FetchArgs, fetchBaseQuery} from "@reduxjs/toolkit/query/react";
import {RootState} from "../store";
import keycloak from "../../Keycloak";


const baseQuery = fetchBaseQuery({
    baseUrl: 'http://192.168.105.139:5005/api/private',
    credentials: 'include',
    prepareHeaders: (headers, {getState}) => {
        const token = (getState() as RootState).user.token
        if (token) {
            headers.set("Authorization", `Bearer ${token}`)
        }
        return headers
    }
})

const baseQueryWithReauth = async (args: string | FetchArgs, api: BaseQueryApi, extraOptions: {}) => {
    let result = await baseQuery(args, api, extraOptions)
    if (result?.error?.status === 401) {
        console.log('sending refresh token')
        // send refresh token to get new access token
        keycloak.onTokenExpired = () => {
            console.log('true')
            keycloak.updateToken(70).then(() => {
                console.log(keycloak.token)
            })
        }
        // if (refreshResult?.data) {
        //     const user = api.getState().auth.user
        //     // store the new token
        //     api.dispatch(setCredentials({...refreshResult.data, user}))
        //     // retry the original query with new access token
        //     result = await baseQuery(args, api, extraOptions)
        // } else {
        //     api.dispatch(logOut())
        // }
    }
    return result
}


export const apiSlice = createApi({
    baseQuery: baseQueryWithReauth,
    tagTypes: ['User'],
    endpoints: () => ({}),
})
