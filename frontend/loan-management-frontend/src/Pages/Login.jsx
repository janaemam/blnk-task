import React, { useState } from 'react';
import { Box, TextField, Button, Typography, Container, InputAdornment } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { Visibility, VisibilityOff } from '@mui/icons-material';
import axios from 'axios';

function Login() {
  const navigate = useNavigate(); // Initialize navigate
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/api/login/', formData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      console.log(response); 
      const role = response.data.role;
      localStorage.setItem('role', role);
      if (role === 'customer') {
        navigate('/customer-home');
      } else if (role === 'fund_provider') {
        navigate('/fund-provider-home');
      } else if (role === 'bank_personnel') {
        navigate('/bank-personnel-home');
      }
    } catch (error) {
      console.error(error.response);  // Handle error (e.g., show error message)
    }
  };

  const handleClickShowPassword = () => {
    setShowPassword(!showPassword);
  };

  const titleStyle = {
    fontSize: 30,
    fontWeight: 700,
    marginTop: '20px',
    textAlign: 'center',
    color: '#242366',
    fontFamily: 'Poppins'
  };

  const textFieldStyle = {
    marginBottom: 2,
    '& .MuiOutlinedInput-root': {
      borderRadius: '20px',
    }
  };

  const rowBoxStyle = {
    justifyContent: 'space-between',
    display: 'flex',
    width: 470,
  };

  return (
    <Box sx={{ backgroundColor: "#f5f5f5", width: '100%', display: 'flex', justifyContent: 'center', height: `calc(100vh - 60px)` }}>
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          mt: 3,
        }}
      >
        <Typography component="h1" gutterBottom sx={titleStyle}>
          Welcome Back!
        </Typography>
        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
          <TextField
            fullWidth
            label="Username"
            name="username"
            value={formData.username}
            onChange={handleChange}
            sx={textFieldStyle}
            required
            type="text"
          />
          <TextField
            fullWidth
            label="Password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            sx={textFieldStyle}
            required
            type={showPassword ? 'text' : 'password'}
          />
          <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
            <Button
              type="submit"
              variant="contained"
              sx={{
                textTransform: 'none',
                fontFamily: 'Poppins',
                backgroundColor: '#242366',
                borderRadius: '20px',
                color: 'white',
                '&:hover': {
                  backgroundColor: '#1e1f58',
                }
              }}
            >
              Log in
            </Button>
          </Box>
        </Box>
      </Box>
    </Box>
  );
}

export default Login;
