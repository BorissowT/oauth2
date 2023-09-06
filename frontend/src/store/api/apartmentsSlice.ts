import {apiSlice} from "./apiSlice";


export const apartmentsSlice = apiSlice.injectEndpoints({
    endpoints: (build) => ({
        getApartments: build.query({
            query: () => 'apartments'
        }),
        deleteApartment: build.mutation({
            query: (id) => ({
                url: `apartments`,
                method: 'DELETE'
            })
        }),
        createApartment: build.mutation({
            query: (apartment) => ({
                url: 'apartments',
                method: 'POST',
                body: apartment
            })
        }),
        changeApartment: build.mutation({
            query: (apartment) => ({
                url: `apartments`,
                method: 'PUT',
                body: apartment
            })
        })
    })
})


export const {
    useDeleteApartmentMutation,
    useCreateApartmentMutation,
    useChangeApartmentMutation
} = apartmentsSlice

export const {useLazyGetApartmentsQuery} = apartmentsSlice