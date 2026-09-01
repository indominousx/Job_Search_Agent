import React from 'react';
import './components.css';

export const GlassCard = ({ children, className = '' }) => {
  return (
    <div className={`glass-panel animate-fade-in ${className}`}>
      {children}
    </div>
  );
};

export const GradientButton = ({ children, onClick, type = 'button', disabled = false, className = '' }) => {
  return (
    <button 
      type={type} 
      onClick={onClick} 
      disabled={disabled}
      className={`gradient-btn ${className}`}
    >
      {children}
    </button>
  );
};

export const TextInput = ({ label, type = 'text', value, onChange, placeholder, className = '' }) => {
  return (
    <div className={`input-group ${className}`}>
      {label && <label className="input-label">{label}</label>}
      <input
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className="text-input"
      />
    </div>
  );
};
