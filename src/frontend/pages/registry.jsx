import { Link, useNavigate } from 'react-router-dom';
import { Button, Footer, fetchFun, Header } from '../functions.jsx';
import '../styles.css';

async function handleRegistry(params) {
    document.getElementById("output").innerHTML = "Pending"
    const result = await fetchFun({
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "login": document.getElementById("login").value,
            "email": document.getElementById("email").value,
            "phone": document.getElementById("phonnumb").value,
            "first_name": document.getElementById("name").value,
            "second_name": document.getElementById("lastname").value,
            "surname": document.getElementById("surname").value,
            "password": document.getElementById("password").value
        }),
        credentials: 'include'
    },"/register")

    if ( result == false){
        
        document.getElementById("output").innerHTML = "Failed no conn."

    }
    else{
        if (result[0].ok){
            document.getElementById("output").innerHTML = "Success"
        }
        else {
            document.getElementById("output").innerHTML = "Error "+result[0].status
        }
    }
}

function Registry() {
    return (
        <>
            <div>
                <Header/>
                <p class="main-text">Регистрация</p>
                <p id="output" class="thick-text"></p>
                <div class="search-group">
                    <p class="main-text">Введите свои данные</p>
                    <input type="text" id="login" placeholder="Логин" /><br></br>
                    <input type="text" id="email" placeholder="Эл. Почта" /><br></br>
                    <input type="text" id="password" placeholder="Пароль" /><br></br><br></br>
                    <input type="text" id="name" placeholder="Имя" /><br></br>
                    <input type="text" id="lastname" placeholder="Фамилия" /><br></br>
                    <input type="text" id="surname" placeholder="Отчество" /><br></br>
                    <input type="text" id="phonnumb" placeholder="Номер телефона" /><br></br>
                    
                    
                    <Button text="Зарегестрироваться" onclick={handleRegistry} /><br></br>
                    {/* <Link to="/login" class="login-link">
                    Уже в системе? Войти
                    </Link> */}
                    <Link style={{ color: 'blue', textDecoration: 'underline' }} to="/login">Уже в системе? Войдите</Link>

                </div>
                <Footer/>
            </div>
        </>
    )
} 

export default Registry