import React from 'react';
import {
    useChangeApartmentMutation,
    useCreateApartmentMutation, useDeleteApartmentMutation,
    useLazyGetApartmentsQuery
} from "../store/api/apartmentsSlice";

const SecuredPage = () => {

    const [createApartment, {data: createData, error: createError}] = useCreateApartmentMutation()
    const [deleteApartment, {data: deleteData, error: deleteError}] = useDeleteApartmentMutation()
    const [changeApartment, {data: changeData, error: changeError}] = useChangeApartmentMutation()
    const [fetchApartments, {data: apartmentsData, error: apartmentsError}] = useLazyGetApartmentsQuery()

    const handleCreateApartment = () => {
        createApartment({name: "New Apartment"})
    }

    const handleDeleteApartment = () => {
        deleteApartment(1)
    }

    const handleChangeApartment = () => {
        changeApartment({id: 1, name: "Changed Apartment"})
    }

    const handleGetApartments = () => {
        fetchApartments('')
    }

    console.log(createError)

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
            <div></div>
        </>
    );
};

export default SecuredPage;