import React from 'react';
import {useLazyExampleQuery} from "../store/api/testApiSlice";
import {useAppSelector} from "../store/store";

const SecuredPage = () => {
    const [trigger, {data}] = useLazyExampleQuery()
    const token = useAppSelector(state => state.user.token)
    const sendRequest = () => {
        trigger()
    }

    return (
        <div>
            {
                data ?
                    // @ts-ignore
                    <p>{data.message}</p>
                    : <></>}
            <h1 className="text-black text-4xl">Welcome to the Protected Page.</h1>
            <button onClick={sendRequest}>Send request</button>
        </div>
    );
};

export default SecuredPage;