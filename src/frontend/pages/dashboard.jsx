import { Link } from 'react-router-dom';
import { Button, Footer, getCookie, setCookie } from '../functions.jsx';
import '../styles.css';

function Lk() {
    return (
        <>
            <div>
                <p class="main-text">Личный кабинет</p>

                <div class="lk-group">
                    <p class="thick-text">Имя: dddddddddddddddddddddddd{getCookie("name")}</p>
                    <p class="thick-text">Должность: {getCookie("role")}</p>
                    <p class="thick-text">лол {getCookie("role")}</p>
                </div>
                <Footer/>
            </div>
        </>
    )
}

export default Lk