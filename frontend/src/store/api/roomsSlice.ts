import {apiSlice} from "./apiSlice";


export const roomsSlice = apiSlice.injectEndpoints({
    endpoints: (build) => ({
        getRooms: build.query<string, void>({
            query: () => 'rooms'
        }),
        deleteRoom: build.mutation({
            query: (id) => ({
                url: `rooms`,
                method: 'DELETE'
            })
        }),
        createRoom: build.mutation({
            query: (room) => ({
                url: 'rooms',
                method: 'POST',
                body: room
            })
        }),
        changeRoom: build.mutation({
            query: (room) => ({
                url: `rooms`,
                method: 'PUT',
                body: room
            })
        })
    })
})

// createMutation for roomsSlice
export const {
    useGetRoomsQuery,
    useDeleteRoomMutation,
    useCreateRoomMutation,
    useChangeRoomMutation
} = roomsSlice

export const {useLazyGetRoomsQuery} = roomsSlice
