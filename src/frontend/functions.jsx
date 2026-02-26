import Cookies from 'js-cookie';
import logo from './assets/logo.png';
import React, { useState, useEffect } from 'react';


const GetStatusStyle = (status) => {
  switch (status.toLowerCase()) {
    case 'готов': return { color: '#2ecc71', fontWeight: 'bold' };
    case 'сдача анализов': return { color: '#f39c12', fontWeight: 'bold' };
    case 'требуется консультация': return { color: '#e74c3c', fontWeight: 'bold' };
    default: return { color: '#333' };
  }
};

export function Button({text,onclick}){
  return (
    <>
      <button type="button" onClick={onclick}>{text}</button>
    </>
  )
}

export async function fetchFun(params,ip) {
  console.log("pendingPost");
  try {
      const response = await fetch("http://155.212.222.12:8000/auth"+ip,params);
      const result = await response.json();

      console.log(result);
      console.log("done POST");
      return [response,result]
  }
  catch(error) {
      console.error("ERROR "+error);
      return false
  }
}

export function Table(){
  const data = [
    { id: 1, client: 'Алекснадр Пушкин', status: 'Готов', DoB: '01/01/70' },
    { id: 2, client: 'Дуэйн Джонс', status: 'Сдача анализов', DoB: '01/01/70' },
    { id: 3, client: 'Дэвид Терри', status: 'Требуется консультация', DoB: '01/01/70' },
    { id: 4, client: 'Зеленский', status: 'Готов', DoB: '01/01/70' },
    { id: 5, client: 'ратмир', status: 'Требуется консультация', DoB: '01/01/70' },
  ];

  return (
    // <table class="table">
    //   <thead>
    //     <tr>
    //       <th class="default-text">Свойство</th>
    //       <th class="default-text">Результат</th>
    //     </tr>
    //   </thead>

    //   <tbody>
    //     {data.map((item) => (
    //       <tr key={item.id}>
    //         <td class="default-text">{item.property}</td>
    //         <td class="default-text">{item.result}</td>
    //       </tr>
    //     ))}
    //   </tbody>
    // </table>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>ФИО</th>
                <th>Статус</th>
                <th>Дата рождения</th>
            </tr>
        </thead>
        <tbody>
            {data.map((item) => (
              <tr key={item.id}>
                <td class="default-text">{item.id}</td>
                <td class="default-text">{item.client}</td>
                <td class="default-text" style = {GetStatusStyle(item.status)}>{item.status}</td>
                <td class="default-text">{item.DoB}</td>
              </tr>
            ))}
        </tbody>
    </table>
  );
}

export function Footer() {
  return (
    <>
      <footer>
        <p class="default-text">Сайт. Все права не защищены</p><br></br>
        
        <a href="/about">О нас</a>
        <a href="/contact">Контакты</a><br></br>
      </footer>
    </>
  )
}

export function Header() {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const handleMouseMove = (e) => {
      if (e.clientY < 70) {
        setIsVisible(true);
      } 

      else if (e.clientY > 150) {
        setIsVisible(false);
      }
    };

    window.addEventListener('mousemove', handleMouseMove);

    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  return (
    <>
      <header class={`header-def ${isVisible ? 'header--visible' : ''}`}>
        <img src={logo} alt="Company Logo" style={{width:'230px', height: 'auto'}} /> 
        <p class="main-text">Офтальмо-Сеть ЯРОКБ</p><br></br>
      </header>
    </>
  );
}

// export function Header() {
//   return (
//     <>
      
//       <header class="header-def">
//         <img src={logo} alt="Company Logo" style={{width:'230px', height: 'auto'}} /> 
//         <p class="main-text">Офтальмо-Сеть ЯРКОБ</p><br></br>
//       </header>
//       <HeaderReveal></HeaderReveal>
//     </>
//   )
// }