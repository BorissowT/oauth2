import React from 'react';
import {
    useChangeApartmentMutation,
    useCreateApartmentMutation, useDeleteApartmentMutation,
    useLazyGetApartmentsQuery
} from "../store/api/apartmentsSlice";
import {
    useChangeRoomMutation,
    useCreateRoomMutation,
    useDeleteRoomMutation,
    useLazyGetRoomsQuery
} from "../store/api/roomsSlice";

/**
 * SecuredPage component.
 * Renders a secured page with buttons to create, delete, update, and get apartments and rooms.
 * Displays error messages if any.
 */
const SecuredPage = () => {

    // Apartment state and mutations
    const [createApartment, {data: createData, error: createError}] = useCreateApartmentMutation()
    const [deleteApartment, {data: deleteData, error: deleteError}] = useDeleteApartmentMutation()
    const [changeApartment, {data: changeData, error: changeError}] = useChangeApartmentMutation()
    const [fetchApartments, {data: apartmentsData, error: apartmentsError}] = useLazyGetApartmentsQuery()
    // Room state and mutations
    const [createRoom, { data: createRoomData, error: createRoomError }] = useCreateRoomMutation();
    const [deleteRoom, { data: deleteRoomData, error: deleteRoomError }] = useDeleteRoomMutation();
    const [changeRoom, { data: changeRoomData, error: changeRoomError }] = useChangeRoomMutation();
    const [fetchRooms, { data: roomsData, error: roomsError }] = useLazyGetRoomsQuery();

    /**
     * Event handler for creating an apartment.
     * Calls the createApartment mutation with a default name.
     */
    const handleCreateApartment = () => {
        createApartment({ name: "New Apartment" });
    };

    /**
     * Event handler for deleting an apartment.
     * Calls the deleteApartment mutation with an apartment ID.
     */
    const handleDeleteApartment = () => {
        deleteApartment(1);
    };

    /**
     * Event handler for updating an apartment.
     * Calls the changeApartment mutation with an apartment ID and a new name.
     */
    const handleChangeApartment = () => {
        changeApartment({ id: 1, name: "Changed Apartment" });
    };

    /**
     * Event handler for fetching apartments.
     * Calls the fetchApartments query to get a list of apartments.
     */
    const handleGetApartments = () => {
        fetchApartments("");
    };

    /**
     * Event handler for creating a room.
     * Calls the createRoom mutation with a default name.
     */
    const handleCreateRoom = () => {
        createRoom({ name: "New Room" });
    };

    /**
     * Event handler for deleting a room.
     * Calls the deleteRoom mutation with a room ID.
     */
    const handleDeleteRoom = () => {
        deleteRoom(1);
    };

    /**
     * Event handler for updating a room.
     * Calls the changeRoom mutation with a room ID and a new name.
     */
    const handleChangeRoom = () => {
        changeRoom({ id: 1, name: "Changed Room" });
    };

    /**
     * Event handler for fetching rooms.
     * Calls the fetchRooms query to get a list of rooms.
     */
    const handleGetRooms = () => {
        fetchRooms()
    }

    return (
        <>
            <h1>Welcome to the Secured Page</h1>
            {/*@ts-ignore*/}
            <p>Get: {apartmentsError ? apartmentsError.data.error_description : apartmentsData?.message}</p>
            {/*@ts-ignore*/}
            <p>Create: {createError ? createError.data.error_description : createData?.message}</p>
            {/*@ts-ignore*/}
            <p>Delete: {deleteError ? deleteError.data.error_description : deleteData?.message}</p>
            {/*@ts-ignore*/}
            <p>Update: {changeError ? changeError.data.error_description : changeData?.message}</p>
            <div>
                <br/>
                <button onClick={handleCreateApartment}>Create Apartment</button>
                <button onClick={handleDeleteApartment}>Delete Apartment</button>
                <button onClick={handleChangeApartment}>Update Apartment</button>
                <button onClick={handleGetApartments}>Get Apartments</button>
            </div>
            <br/>
            {/*@ts-ignore*/}
            <p>Get: {roomsError ? roomsError.data.error_description : roomsData?.message}</p>
            {/*@ts-ignore*/}
            <p>Create: {createRoomError ? createRoomError.data.error_description : createRoomData?.message}</p>
            {/*@ts-ignore*/}
            <p>Delete: {deleteRoomError ? deleteRoomError.data.error_description : deleteRoomData?.message}</p>
            {/*@ts-ignore*/}
            <p>Update: {changeRoomError ? changeRoomError.data.error_description : changeRoomData?.message}</p>
            <div>
                <br/>
                <button onClick={handleCreateRoom}>Create Room</button>
                <button onClick={handleDeleteRoom}>Delete Room</button>
                <button onClick={handleChangeRoom}>Update Room</button>
                <button onClick={handleGetRooms}>Get Rooms</button>
            </div>
        </>
    );
};

export default SecuredPage;