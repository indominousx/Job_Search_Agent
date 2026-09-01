import React, { useState, useRef } from 'react';
import { GlassCard, GradientButton } from './UI';
import { UploadCloud, FileText, CheckCircle } from 'lucide-react';

export const ResumeUpload = () => {
  const [file, setFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadSuccess, setUploadSuccess] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setUploadSuccess(false);
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    setIsUploading(true);
    
    // Simulating API call to POST /api/v1/resume/upload
    // In a real implementation, we would construct FormData and use fetch/axios
    setTimeout(() => {
      setIsUploading(false);
      setUploadSuccess(true);
      setFile(null);
      // Wait 3 seconds then reset success message
      setTimeout(() => setUploadSuccess(false), 3000);
    }, 1500);
  };

  return (
    <GlassCard>
      <div className="flex items-center gap-2 mb-4">
        <FileText size={24} color="var(--accent-secondary)" />
        <h2>Resume Upload</h2>
      </div>
      <p className="mb-4" style={{ color: 'var(--text-secondary)' }}>
        Upload your latest PDF or DOCX resume. The agent will parse it and use it as your definitive Candidate Profile for all job applications.
      </p>

      <div 
        className="upload-zone"
        onClick={() => fileInputRef.current?.click()}
        style={{
          border: '2px dashed var(--glass-border)',
          borderRadius: '12px',
          padding: '2rem',
          textAlign: 'center',
          cursor: 'pointer',
          background: 'rgba(0,0,0,0.1)',
          transition: 'all 0.3s ease',
          marginBottom: '1rem'
        }}
      >
        <input 
          type="file" 
          ref={fileInputRef} 
          onChange={handleFileChange} 
          accept=".pdf,.docx" 
          style={{ display: 'none' }} 
        />
        <UploadCloud size={48} color="var(--text-secondary)" style={{ margin: '0 auto 1rem' }} />
        {file ? (
          <p style={{ fontWeight: 500 }}>Selected: {file.name}</p>
        ) : (
          <p style={{ color: 'var(--text-secondary)' }}>Click to browse or drag and drop<br/>(PDF, DOCX up to 5MB)</p>
        )}
      </div>

      <div className="flex justify-between items-center">
        <span style={{ color: 'var(--success)', display: 'flex', alignItems: 'center', gap: '0.5rem', opacity: uploadSuccess ? 1 : 0, transition: 'opacity 0.3s' }}>
          <CheckCircle size={18} /> Uploaded & Parsed Successfully!
        </span>
        <GradientButton 
          onClick={handleUpload} 
          disabled={!file || isUploading}
        >
          {isUploading ? 'Parsing...' : 'Upload & Parse'}
        </GradientButton>
      </div>
    </GlassCard>
  );
};
