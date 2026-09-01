import React, { useState, useEffect } from 'react';
import { GlassCard, TextInput, GradientButton } from './UI';
import { Key, Save } from 'lucide-react';

export const ApiConfig = () => {
  const [geminiKey, setGeminiKey] = useState('');
  const [groqKey, setGroqKey] = useState('');
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    // Load from local storage on mount
    const gKey = localStorage.getItem('GEMINI_API_KEY') || '';
    const qKey = localStorage.getItem('GROQ_API_KEY') || '';
    setGeminiKey(gKey);
    setGroqKey(qKey);
  }, []);

  const handleSave = () => {
    localStorage.setItem('GEMINI_API_KEY', geminiKey);
    localStorage.setItem('GROQ_API_KEY', groqKey);
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <GlassCard>
      <div className="flex items-center gap-2 mb-4">
        <Key size={24} color="var(--accent-primary)" />
        <h2>API Configuration</h2>
      </div>
      <p className="text-secondary mb-4" style={{ color: 'var(--text-secondary)' }}>
        Provide your API keys to power the Job Agent. Gemini is used as the primary engine, falling back to Groq. Keys are stored locally in your browser.
      </p>
      
      <div className="grid gap-4 mb-4">
        <TextInput 
          label="Gemini API Key (Primary)" 
          type="password"
          placeholder="AIzaSy..." 
          value={geminiKey}
          onChange={(e) => setGeminiKey(e.target.value)}
        />
        <TextInput 
          label="Groq API Key (Fallback)" 
          type="password"
          placeholder="gsk_..." 
          value={groqKey}
          onChange={(e) => setGroqKey(e.target.value)}
        />
      </div>

      <div className="flex justify-between items-center mt-4">
        <span style={{ color: 'var(--success)', opacity: saved ? 1 : 0, transition: 'opacity 0.3s' }}>
          Keys saved securely!
        </span>
        <GradientButton onClick={handleSave}>
          <Save size={18} /> Save Keys
        </GradientButton>
      </div>
    </GlassCard>
  );
};
