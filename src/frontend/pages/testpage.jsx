import {fetchFun,Button} from '../functions.jsx';
import Cookies from 'js-cookie';
async function test() {
    const dotests = await fetchFun({headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        credentials: 'include'
    },"/get_me")
}

function maind() {
    return (
        <>
            <Button text={"test"} onclick={test}/>
        </>
    )
}


export default maind