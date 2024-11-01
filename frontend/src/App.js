// frontend/src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './Components/Login';
import Signup from './Components/Signup';
import Home from './Pages/Home';
import Navbar from './Components/Navbar';
import FaceRecog from './Components/FaceRecog';

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/" element={<Home />} />
        <Routes path="/cam1" element={<FaceRecog />} />
      </Routes>
    </Router>
  );
}

export default App;
