// src/App.js
import React from 'react';
import './App.css';
import ResponsiveAppBar from './Components/Appbar';
import Landing from './Pages/Landing';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ProtectedRoute from './Hooks/protectedRoute';
import CustomerRegister from './Pages/CustomerRegister';
import Login from './Pages/Login'
import BankPersonnelHome from './Pages/BankPersonnelHome';
import FundProviderHome from './Pages/FundProviderHome';
import CustomerHome from './Pages/CustomerHome'

const App = () => {
  return (
    <Router>
      <ResponsiveAppBar />
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/register" element={<CustomerRegister />} />
        <Route path="/login" element={<Login/>} />
        <Route path="/customer-home" element={<CustomerHome/>}/>
        <Route path="/fund-provider-home" element={<FundProviderHome/>} />
        <Route path="/bank-personnel-home" element={<BankPersonnelHome/>}/>
        {/* <Route path="/about" element={<About />} /> */}
        {/* Add more routes as needed */}
      </Routes>
    </Router>
  );
};

export default App;
