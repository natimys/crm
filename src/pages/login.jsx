import { Link, Route } from 'react-router-dom';
import { Button, Footer } from '../functions.jsx';
import '../styles.css';

function Login() {
    const handleLogin = () => {<Route path="/login" element={<Login />} />};
    return (
    <>
        <div>
            <p class="main-text">Логин</p>
            <p id="output" class="thick-text"></p>
            <div class="search-group">
                <p class="main-text">Введите свои данные</p>
                <input type="text" id="phonnumb" placeholder="Номер телефона" /><br></br>
                <input type="text" id="email" placeholder="Эл. Почта" /><br></br>
                
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