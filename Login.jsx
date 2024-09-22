import React from 'react';
import './Login.css';
import { FaRegUserCircle } from "react-icons/fa";
import { FaLock } from "react-icons/fa";


const Login = () => {
  return (
    <div className='wrapper'>
        <form action="">
            <h1>Login</h1>
            <div className="input-box">
                <input type="text" placeholder='Username' required />
                <FaRegUserCircle className='icon' />
             </div>
            <div className="input-box">
                <input type="Password" placeholder='Password' required />
                <FaLock className='icon'/>
            </div>

            <div className="remember-forgot">
                <label><input type="checkbox"/>Remember me</label>
                <a href="#">Forgot password?</a>
            </div>
            <button type="submit">Login</button>

        </form>

    </div>
  );
};

export default Login;