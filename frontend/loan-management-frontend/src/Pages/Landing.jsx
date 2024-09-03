import {Container, Typography, Button,Box, AppBar} from "@mui/material"
import { useNavigate } from 'react-router-dom';
import register from "../assets/register.svg";
function Landing(){
    const navigate = useNavigate(); // Initialize navigate
    const titleStyle={
        fontSize: 30,
        fontWeight:700,
        marginTop: '20px',
        textAlign: 'center',
        color:' #242366',
        fontFamily:'Poppins'

    }
    const buttonStyle={
        display: 'flex',
        justifyContent: 'center',
        borderRadius:20,
        // color:"#6AABDD",
        backgroundColor:"#242366",
        color:'white',
        textTransform:'none',
        mx:1,
        p:2,
        height:30,
        border:"#6AABDD",
         fontFamily:'Poppins'
    }
    const boxStyle={
        display: 'flex',
        flexDirection:'row',
        // width:'80%',
        padding:4,
        justifyContent: 'center',


    }
    const mainBoxStyle={
        height:`calc(100vh - 60px)`,
        backgroundColor:'#f5f5f5',
        padding:3,
    }
    const buttonBoxStyle={
        display:'flex',
        flexDirection:'column',
        width:'300px',
        justifyContent:'center',
        alignItems:'center',
    }
    return(
        <>
        <Box sx={mainBoxStyle}>
            <Typography variant="h1" sx={titleStyle}>Welcome to Blnk</Typography>
            <Box sx={boxStyle}>
                <img src={register} alt="Icon" width="700" height="300" />
                <Box sx={buttonBoxStyle}>
                    <Typography sx={{fontWeight:700, textAlign:"center", fontSize:30, color:' #242366', fontFamily:'Poppins'}}> Join us now! </Typography>
                    <Typography sx={{textAlign:'center', fontFamily:'Poppins'}}>
                       Get your loan in minutes. Buy what you want when you want it.
                    </Typography>
                    <Box sx={{display:'flex', flexDirection:'row', my:3}}>
                      <Button sx={buttonStyle} onClick={() => navigate('/register')}>Register</Button>
                     <Button sx={buttonStyle} onClick={() => navigate('/login')}>Log In</Button>
                    </Box>

                </Box>

            </Box>

        </Box>
        </>
    )

}
export default Landing;