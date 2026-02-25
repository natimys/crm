import { Routes, Route, BrowserRouter, Navigate } from 'react-router-dom';
import './styles.css';
import Registry from './pages/registry';
import Login from './pages/login'; 


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/registry" />} />
        
        <Route path="/registry" element={<Registry />} />
        
        <Route path="/login" element={<Login />} />
        
        {/* Можно добавить страницу 404 */}
        <Route path="*" element={<h1 class="main-text">404: Страница не найдена</h1>} />
      </Routes>
    </BrowserRouter>
  );
}


export default App
