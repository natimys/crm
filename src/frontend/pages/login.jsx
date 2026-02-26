import { Link, Route } from 'react-router-dom';
import Cookies from 'js-cookie';
import { Button, Footer, fetchFun, Header } from '../functions.jsx';
import '../styles.css';

async function handleLogin(params) {
    document.getElementById("output").innerHTML = "Pending"
    const result = await fetchFun({
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "login": document.getElementById("login").value,
            "password": document.getElementById("password").value,
        }),
        credentials: 'include'
    },"/login")
    console.log(result[1].access_token);
    if ( result == false){
        document.getElementById("output").innerHTML = "Failed no conn."
    }
    else{
        if (result[0].ok){
            document.getElementById("output").innerHTML = "Success"
            Cookies.set("access_token",result[1].access_token,30)
        }
        else {
            document.getElementById("output").innerHTML = "Error "+result[0].status
        }
    }
    
}

function Login() {
    return (
    <>
        <div>
            <Header/>
            <p class="main-text">Логин</p>
            <p id="output" class="thick-text"></p>
            <div class="search-group">
                <p class="main-text">Введите свои данные</p>
                <input type="text" id="login" placeholder="Логин" /><br></br>
                <input type="text" id="password" placeholder="Пароль" /><br></br>
                
                <Button text="Войти" onclick={handleLogin} /><br></br>
                {/* <Link to="/login" class="login-link">
                Уже в системе? Войти
                </Link> */}
                <Link style={{ color: 'blue', textDecoration: 'underline' }} to="/registry">Ещё не вошли? Зарегестрируйтесь</Link>
                
            </div>
            <Footer/>
        </div>
    </>
    )
} 

export default Login