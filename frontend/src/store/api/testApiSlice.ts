import {apiSlice} from "./apiSlice";


export const testApiSlice = apiSlice.injectEndpoints({
    endpoints: (build) => ({
        example: build.query<void, void>({
            query: () => ''
        })
    })
})


export const {useExampleQuery, useLazyExampleQuery} = testApiSlice