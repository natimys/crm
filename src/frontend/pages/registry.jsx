import { Link, useNavigate } from 'react-router-dom';
import { Button, Footer } from '../functions.jsx';
import '../styles.css';

function Registry() {
    const navigate = useNavigate();
    const handleLogin = () => {navigate('/login')};
    return (
        <>
            <div>
                <p class="main-text">Регистрация</p>
                <p id="output" class="thick-text"></p>
                <div class="search-group">
                    <p class="main-text">Введите свои данные</p>
                    <input type="text" id="name" placeholder="Имя" /><br></br>
                    <input type="text" id="lastname" placeholder="Фамилия" /><br></br>
                    <input type="text" id="subname" placeholder="Отчество" /><br></br>
                    <input type="text" id="phonnumb" placeholder="Номер телефона" /><br></br>
                    <input type="text" id="email" placeholder="Эл. Почта" /><br></br>
                    
                    <Button text="Зарегестрироваться" onclick={handleLogin} /><br></br>
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