// frontend/src/Pages/Home.js
import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const Home = () => {
  const navigate = useNavigate();

  useEffect(() => {
    // Check for the token in localStorage
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
    }
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.href = '/login';
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gradient-to-r from-red-600 to-black overflow-hidden relative">
      <div className="bg-white bg-opacity-20 backdrop-blur-md border border-white border-opacity-30 rounded-xl p-8 shadow-lg z-10">
        <h1 className="lg:text-2xl text-[1.4rem] font-bold text-white">Welcome to AI Surveillance</h1>
        <h2 className="lg:text-lg text-[1.2rem] text-gray-200 mt-2">Monitoring with Precision</h2>
        <p className="lg:text-[1rem] text-[0.8rem] text-gray-300 mt-4">
          You're now logged in and ready to experience the future of AI-powered surveillance.
        </p>
        <button 
          onClick={handleLogout} 
          className="mt-4 bg-red-500 text-white py-2 px-4 rounded hover:bg-red-600 transition duration-200"
        >
          Logout
        </button>
      </div>
      <div className="absolute inset-0 pointer-events-none">
        <div className="animate-bounce w-16 h-16 bg-white rounded-full opacity-20" style={{ animationDuration: '5s', top: '30%', left: '20%' }} />
        <div className="animate-bounce w-24 h-24 bg-white rounded-full opacity-20" style={{ animationDuration: '7s', top: '60%', left: '50%' }} />
        <div className="animate-bounce w-20 h-20 bg-white rounded-full opacity-20" style={{ animationDuration: '6s', top: '20%', left: '70%' }} />
      </div>
    </div>
  );
};

export default Home;
