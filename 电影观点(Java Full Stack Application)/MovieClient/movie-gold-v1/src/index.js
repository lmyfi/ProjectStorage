import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import 'bootstrap/dist/css/bootstrap.min.css'; //这个没有导入的问题，对于我第一次接触React构建前端页面来说，踩了很久的坑，因为没有导入这个，导致我编辑导航栏时出现了布局混乱
import { BrowserRouter,Routes, Route } from 'react-router-dom';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path='/*' element={<App />}></Route>
      </Routes>
    </BrowserRouter>
    
  </React.StrictMode>
);


// import React from 'react';
// import ReactDOM from 'react-dom/client';
// import './index.css';
// import App from './App';
// import 'bootstrap/dist/css/bootstrap.min.css';
// import { BrowserRouter, Route, Routes } from 'react-router-dom';


// const root = ReactDOM.createRoot(document.getElementById('root'));
// root.render(
//   <React.StrictMode>
//     <BrowserRouter>
//       <Routes>
//           <Route path="/*" element={<App />} />
//       </Routes>
//     </BrowserRouter>
//   </React.StrictMode>
// );



