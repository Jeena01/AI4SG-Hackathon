import React from 'react';
import './Header.css';

function Header() {
  return (
    <header className="header">
      <div className="logo">
        Cultural Care Compass
      </div>
      <nav className="nav">
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/clients">Clients</a></li>
          <li><a href="/employees">Employees</a></li>
        </ul>
      </nav>
    </header>
  );
}

export default Header;
