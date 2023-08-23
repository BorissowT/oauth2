import {User, UserState} from "../../types/users";
import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import {RootState} from "../store";

const initialState: UserState = {
    user: null,
    token: null
}

export const userSlice = createSlice({
    name: 'user',
    initialState,
    reducers: {
        setCredentials(state, action: PayloadAction<{user: User, token: string}>) {
            state.user = action.payload.user
            state.token = action.payload.token
        },
        logOut(state, action) {
            state.user = null;
            state.token = null;
        }
    }
})

export const { setCredentials, logOut } = userSlice.actions

export const selectUser = (state: RootState) => state.user.user

export default userSlice.reducer
