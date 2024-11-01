// frontend/src/Components/Navbar.js
import React from 'react';

const Navbar = () => {
  const handleNavigation = (path) => {
    window.location.href = path;
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.href = '/login';
  };

  return (
    <nav className="fixed top-0 left-0 w-full h-[5rem] bg-white bg-opacity-20 backdrop-blur-md border-b border-white border-opacity-30 shadow-md z-20">
      <div className="max-w-7xl mx-auto px-6 py-2 flex justify-between items-center h-full">
        {/* Logo */}
        <div className="flex items-center">
          <img 
            src="/path/to/logo.png" // Replace with your logo path
            alt="Logo" 
            className="h-10 w-10 mr-3"
          />
          <h1 className="text-2xl font-bold text-white cursor-pointer" onClick={() => handleNavigation('/')}>
            AI Surveillance
          </h1>
        </div>

        {/* Navigation Links */}
        <ul className="flex space-x-8 text-lg font-semibold">
          <li
            className="text-white cursor-pointer hover:text-gray-300 transition duration-200"
            onClick={() => handleNavigation('/')}
          >
            Home
          </li>
          <li
            className="text-white cursor-pointer hover:text-gray-300 transition duration-200"
            onClick={() => handleNavigation('/cam1')}
          >
            Cam1
          </li>
          <li
            className="text-white cursor-pointer hover:text-gray-300 transition duration-200"
            onClick={() => handleNavigation('/cam2')}
          >
            Cam2
          </li>
          <li
            className="text-white cursor-pointer hover:text-gray-300 transition duration-200"
            onClick={() => handleNavigation('/cam3')}
          >
            Cam3
          </li>
        </ul>

        {/* Logout Button */}
        <button 
          onClick={handleLogout} 
          className="text-white bg-red-500 py-1 px-4 rounded-lg hover:bg-red-600 transition duration-200"
        >
          Logout
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
