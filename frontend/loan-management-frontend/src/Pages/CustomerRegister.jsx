import React, { useState } from 'react';
import { Box, TextField, Button, Typography, Container, IconButton, InputAdornment } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { Visibility, VisibilityOff } from '@mui/icons-material';
import axios from 'axios';
function CustomerRegister() {
  const navigate = useNavigate(); // Initialize navigate
  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({
    first_name: '',
    username:'',
    last_name: '',
    email: '',
    confirm_password: '',
    balance: '',
    credit_score: '800',
    salary: '',
    age: '',
    dependents: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: name === 'balance' || name === 'salary' || name === 'age'
        ? Math.max(0, value)
        : value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    // Submit the form data to the backend
    try {
      const response = await axios.post('http://localhost:8000/api/register/', formData, {
        headers: {
          'Content-Type': 'application/json',
        },
      });
      console.log(response);  // Handle success (e.g., navigate to another page or show a success message)
      navigate('/login')
    } catch (error) {
      console.error(error.response);  // Handle error (e.g., show error message)
    }

  };
  const handleClickShowPassword = () => {
    setShowPassword(!showPassword);
  };
  const titleStyle={
    fontSize: 30,
    fontWeight:700,
    marginTop: '20px',
    textAlign: 'center',
    color:' #242366',
    fontFamily:'Poppins'

}
  const textFieldStyle = {
    // width: '100%',
  

    marginBottom: 2,
    '& .MuiOutlinedInput-root': {
      borderRadius: '20px',
    }
  };
  const rowBoxStyle={
    justifyContent:'space-between',
     display:'flex',
      width:470,
  }
  return (
    <Box sx={{backgroundColor:"#f5f5f5", width:'100%', display:'flex', justifyContent:'center',  height:`calc(100vh - 60px)`,}}>
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          mt: 3,
        }}
      >
        <Typography component="h1" gutterBottom sx={titleStyle}>
          Customer Registration
        </Typography>
        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
          <Box sx={rowBoxStyle}>
          <TextField
            label="First Name"
            name="first_name"
            value={formData.fname}
            onChange={handleChange}
            sx={textFieldStyle}
            required
          />
          <TextField
            label="Last Name"
            name="last_name"
            value={formData.lname}
            onChange={handleChange}
            sx={textFieldStyle}
            required
          />
          </Box>
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
            label="Email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            sx={textFieldStyle}
            required
            type="email"
          />
          <Box sx={rowBoxStyle}>
          <TextField
            label="Password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            sx={textFieldStyle}
            required
            type={showPassword ? 'text' : 'password'} 
            endAdornment={
              <InputAdornment position="end">
                <Visibility />
              </InputAdornment>
            }      
          />
            <TextField
            label="Confirm"
            name="confirm_password"
            value={formData.confirm_password}
            onChange={handleChange}
            sx={textFieldStyle}
            required
            type={showPassword ? 'text' : 'password'} 
            endAdornment={
              <InputAdornment position="end">
                <Visibility />
              </InputAdornment>
            }      
          />
          </Box>
         
          <Box sx={rowBoxStyle} >
          <TextField
            label="Balance"
            name="balance"
            value={formData.balance}
            onChange={handleChange}
            sx={textFieldStyle}
            required
            type="number"
          />
          <TextField
            label="Salary"
            name="salary"
            value={formData.salary}
            onChange={handleChange}
            sx={textFieldStyle}
            required
            type="number"
          />
          </Box>
          <Box sx={rowBoxStyle}>
          <TextField
            label="Age"
            name="age"
            value={formData.age}
            onChange={handleChange}
            sx={textFieldStyle}
            required
            type="number"
          />
          <TextField
            label="No. of Dependents"
            name="dependents"
            value={formData.dependents}
            onChange={handleChange}
            sx={textFieldStyle}
            required
            type="number"
          />
          </Box>

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
              Register
            </Button>
          </Box>
        </Box>
      </Box>
    </Box>
  );
}

export default CustomerRegister;