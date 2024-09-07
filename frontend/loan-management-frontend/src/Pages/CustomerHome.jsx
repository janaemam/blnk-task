import React, { useEffect, useState } from 'react';
import { Typography, Box, TextField, Button, MenuItem, Select, FormControl, InputLabel } from '@mui/material';
import axios from 'axios';

function CustomerHome() {
    const [loanPlans, setLoanPlans] = useState([]);
    const [selectedPlan, setSelectedPlan] = useState('');
    const [principal, setPrincipal] = useState('');
    const [total, setTotal] = useState('');
    const [error, setError] = useState('');
    
    const mainBoxStyle = {
        height: `calc(100vh - 60px)`,
        backgroundColor: '#f5f5f5',
        padding: 3,
        display: "flex",
        flexDirection: 'column',
        alignItems: "center",
    };

    const titleStyle = {
        fontSize: 30,
        fontWeight: 700,
        marginTop: '20px',
        textAlign: 'center',
        color: '#242366',
        fontFamily: 'Poppins'
    };

    useEffect(() => {
        // Fetch loan plans
        axios.get('http://localhost:8000/api/loan-plans/',{ withCredentials: true })
            .then(response => setLoanPlans(response.data))
            .catch(error => setError('Error fetching loan plans'));
    }, []);

    const handlePrincipalChange = (e) => {
        const value = e.target.value;
        setPrincipal(value);
        if (selectedPlan) {
            const plan = loanPlans.find(p => p.id === selectedPlan);
            if (plan) {
                const interestRate = plan.interest_rate;
                const calculatedTotal = value * (1 + (interestRate / 100));
                setTotal(calculatedTotal.toFixed(2));
            }
        }
    };

    const handlePlanChange = (e) => {
        setSelectedPlan(e.target.value);
        setPrincipal('');
        setTotal('');
    };

    const handleApply = () => {
        if (principal && selectedPlan) {
            axios.post('/api/loan-requests/apply/', {
                loan_plan: selectedPlan,
                principal: parseFloat(principal),
                total: parseFloat(total)
            })
            .then(response => {
                alert('Loan application submitted successfully');
                setPrincipal('');
                setSelectedPlan('');
                setTotal('');
            })
            .catch(error => setError('Error submitting loan application'));
        } else {
            setError('Please fill in all fields');
        }
    };

    return (
        <Box sx={mainBoxStyle}>
            <Typography sx={titleStyle}>
                What do you want to do today?
            </Typography>
            <Box sx={{ marginTop: 4, width: '100%', maxWidth: 600 }}>
                <FormControl fullWidth margin="normal">
                    <InputLabel>Loan Plan</InputLabel>
                    <Select
                        value={selectedPlan}
                        onChange={handlePlanChange}
                        label="Loan Plan"
                    >
                        {loanPlans.map(plan => (
                            <MenuItem key={plan.id} value={plan.id}>
                                {plan.name} - Interest Rate: {plan.interest_rate}%
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>
                <TextField
                    label="Principal Amount"
                    type="number"
                    value={principal}
                    onChange={handlePrincipalChange}
                    fullWidth
                    margin="normal"
                />
                <TextField
                    label="Total Amount After Interest"
                    value={total}
                    InputProps={{ readOnly: true }}
                    fullWidth
                    margin="normal"
                />
                {error && <Typography color="error">{error}</Typography>}
                <Button
                    variant="contained"
                    color="primary"
                    onClick={handleApply}
                    fullWidth
                    sx={{ marginTop: 2 }}
                >
                    Apply for Loan
                </Button>
            </Box>
        </Box>
    );
}

export default CustomerHome;
