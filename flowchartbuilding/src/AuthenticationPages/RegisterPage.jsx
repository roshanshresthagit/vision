import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEye, faEyeSlash } from '@fortawesome/free-regular-svg-icons';
import "./RegisterPage.css";
import api from "../api.js";

const RegisterPage = () => {
  const [error, setError] = useState("");
  
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });

  const [showPassword, setShowPassword] = useState({
    password: false,
    confirmPassword: false,
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const togglePasswordVisibility = (field) => {
    setShowPassword((prevState) => ({
      ...prevState,
      [field]: !prevState[field],
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Form submitted:', formData);
    try{
      const response = await api.post('/register_user', formData)
      console.log("this is response", response)
      if (response.data.success){
        navigate("/login")
      }else{
        setError("User not registered")
      }
    }catch (error){
      setError("An error occured Please try again.")
    }
  };

  return (
    <div>
      <div className="register-page">
        <div className="register-container">
          <div className="header">
            <h1 className="header-title">Register</h1>
            <div className="have-account">
              Already have an account? <a href="/login">Login</a>
            </div>
          </div>

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="email" className="label">Email</label>
              <input
                type="email"
                id="email"
                name="email"
                placeholder="Enter your email"
                value={formData.email}
                onChange={handleChange}
                className="input"
              />
            </div>

            <div className="form-group">
              <label htmlFor="password" className="label">Password</label>
              <div className="input-group">
                <input
                  type={showPassword.password ? 'text' : 'password'}
                  id="password"
                  name="password"
                  placeholder="Enter your password"
                  value={formData.password}
                  onChange={handleChange}
                  className="input"
                />
                <button
                  type="button"
                  className="toggle-password"
                  onClick={() => togglePasswordVisibility('password')}
                >
                  <FontAwesomeIcon icon={showPassword.password ? faEye : faEyeSlash} />
                </button>
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="confirm-password" className="label">Confirm Password</label>
              <div className="input-group">
                <input
                  type={showPassword.confirmPassword ? 'text' : 'password'}
                  id="confirm-password"
                  name="confirmPassword"
                  placeholder="Confirm your password"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  className="input"
                />
                <button
                  type="button"
                  className="toggle-password"
                  onClick={() => togglePasswordVisibility('confirmPassword')}
                >
                  <FontAwesomeIcon icon={showPassword.confirmPassword ? faEye : faEyeSlash} />
                </button>
              </div>
            </div>
            {error && <div className="error-message">{error}</div>}
            <button type="submit" className="register-btn">Register</button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;
