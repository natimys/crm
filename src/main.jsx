// function lol(logs){
//     console.log("do anything "+logs)
// }
const ip = "https://mocktarget.apigee.net/echo"
async function fetchFun(params) {
    try {
        const response = await fetch(ip,params);
        const result = await response.json();

        console.log(result);
        console.log("success");
        return result
    }
    catch(error) {
        console.error("ERROR "+error);
        return false
    }
}

async function registration() {
    document.getElementById("output").textContent = "Pending..."
    const fetchResult = await fetchFun({
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({"name": document.getElementById("name").value, "age": document.getElementById("age").value, "secret_name": document.getElementById("secname").value})
    });
    if (fetchResult == false){
        document.getElementById("output").textContent = "Error, please try again later."
    }
    else{
        console.log(fetchResult)
        document.getElementById("output").textContent = "Success!"
    }
}


