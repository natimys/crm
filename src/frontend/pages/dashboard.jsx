import { Button, Footer, Table, Header } from '../functions.jsx';
import '../styles.css';


function Lk() {
    return (
        <>
        <Header/>
        <body class="body-dashboard">
            
            <div class="container">
                <p class="main-text">Дэшборд</p>
                <header class="stats-grid">
                    <div class="card blue">
                        <h3>Пациенты</h3>
                        <p>40</p>
                    </div>
                    <div class="card green">
                        <h3>Готовы к операции</h3>
                        <p>3</p>
                    </div>
                    <div class="card orange">
                        <h3>В процессе сдачи анализов</h3>
                        <p>452</p>
                    </div>
                    <div class="card red">
                        <h3>Требующих консультации</h3>
                        <p>4325</p>
                    </div>
                </header>

                <main class="table-container">
                    <h2 class="thick-text">Список пациентов</h2>
                    <Table></Table>
                </main>
                
            </div>
        </body>
        <Footer/>
        </>
    )
}

export default Lk