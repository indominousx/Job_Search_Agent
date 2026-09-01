import React from 'react';
import { ApiConfig } from './components/ApiConfig';
import { ResumeUpload } from './components/ResumeUpload';
import { GlassCard } from './components/UI';
import { Play } from 'lucide-react';
import './index.css';

function App() {
  return (
    <div className="container">
      <header className="mb-4" style={{ textAlign: 'center', padding: '2rem 0' }}>
        <h1 style={{ fontSize: '2.5rem', background: 'linear-gradient(135deg, #fff, #94a3b8)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
          Job Agent Control Plane
        </h1>
        <p style={{ color: 'var(--text-secondary)' }}>Autonomous AI Career Orchestration</p>
      </header>

      <div className="grid md:grid-cols-2">
        <ApiConfig />
        <ResumeUpload />
      </div>

      <div className="mt-8">
        <GlassCard>
          <div className="flex items-center justify-between">
            <div>
              <h2>Job Intelligence Pipeline</h2>
              <p style={{ color: 'var(--text-secondary)' }}>Status: IDLE — Ready to scan for jobs and prepare applications.</p>
            </div>
            <button className="gradient-btn" style={{ padding: '1rem 2rem', fontSize: '1.1rem' }}>
              <Play size={20} /> Run Workflow Now
            </button>
          </div>
          
          <div style={{ marginTop: '2rem', padding: '3rem', textAlign: 'center', border: '1px dashed var(--glass-border)', borderRadius: '12px' }}>
            <p style={{ color: 'var(--text-secondary)' }}>No recent application data found. Click 'Run Workflow Now' to discover and match jobs.</p>
          </div>
        </GlassCard>
      </div>
    </div>
  );
}

export default App;
