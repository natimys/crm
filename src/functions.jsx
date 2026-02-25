export function Button({text,onclick}){
  return (
    <>
      <button type="button" onClick={onclick}>{text}</button>
    </>
  )
}

export function Footer() {
  return (
    <>
      <footer>
        <div class="footer-group">
          <p class="default-text">Сайт. Все права не защищены</p><br></br>
          
          <a href="/about">О нас</a>
          <a href="/contact">Контакты</a><br></br>
        </div>
      </footer>
    </>
  )
}