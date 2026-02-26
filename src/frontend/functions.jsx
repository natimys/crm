import Cookies from 'js-cookie';

export function Button({text,onclick}){
  return (
    <>
      <button type="button" onClick={onclick}>{text}</button>
    </>
  )
}

export function getCookie({target}){
  return Cookies.get(target)
}

export function setCookie({target, value, expire}){
  Cookies.set(target, value, expire)
}

export function Footer() {
  return (
    <>
      <footer class="footer-group">
        <p class="default-text">Сайт. Все права не защищены</p><br></br>
        
        <a href="/about">О нас</a>
        <a href="/contact">Контакты</a><br></br>
      </footer>
    </>
  )
}