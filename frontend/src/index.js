import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import './index.css';
import App from './App';

// Set page title
document.title = "CoverCraft - Crafting personalized cover letters that make you stand out";

// Set favicon
const iconLink = document.createElement("link");
iconLink.rel = "stylesheet";
iconLink.href = "https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&icon_names=stylus_laser_pointer";
document.head.appendChild(iconLink);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <BrowserRouter>
    <App />
  </BrowserRouter>
);
