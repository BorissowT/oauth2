export interface User {
    id: number,
    name: string,
    email: string,
    username: string,
    addresses: string,
    chosenLanguage: "de" | "en",
}

export interface UserState {
    user: null | User,
    token: string | null // access token
}
