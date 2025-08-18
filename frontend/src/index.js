import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import './index.css';
import App from './App';

// Set page title
document.title = "CoverCraft - Crafting personalized cover letters that make you stand out";

// Set favicon
const link = document.createElement("link");
link.rel = "icon";
link.href = "/CoverCraft-fav.png"; 
document.head.appendChild(link);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <BrowserRouter>
    <App />
  </BrowserRouter>
);
