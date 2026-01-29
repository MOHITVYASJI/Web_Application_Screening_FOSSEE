/**
 * Upload Section Component
 */

import React, { useState, useRef } from 'react';
import {
  Button,
  CircularProgress,
  LinearProgress,
  Paper,
  Typography,
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { datasetAPI } from '../../services/api';

function UploadSection({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [dragging, setDragging] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileSelect = (selectedFile) => {
    setError('');
    setSuccess('');

    // Validate file type
    if (!selectedFile.name.endsWith('.csv')) {
      setError('Please select a CSV file');
      return;
    }

    // Validate file size (5MB max)
    if (selectedFile.size > 5 * 1024 * 1024) {
      setError('File size must be less than 5MB');
      return;
    }

    setFile(selectedFile);
  };

  const handleFileInputChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      handleFileSelect(selectedFile);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);

    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      handleFileSelect(droppedFile);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragging(true);
  };

  const handleDragLeave = () => {
    setDragging(false);
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file first');
      return;
    }

    setUploading(true);
    setError('');
    setSuccess('');
    setUploadProgress(0);

    try {
      const data = await datasetAPI.uploadCSV(file, (progressEvent) => {
        const progress = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        );
        setUploadProgress(progress);
      });

      setSuccess('File uploaded and processed successfully!');
      setFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }

      // Notify parent component
      if (onUploadSuccess) {
        onUploadSuccess(data);
      }
    } catch (err) {
      const errorMessage =
        err.response?.data?.error ||
        err.response?.data?.file?.[0] ||
        'Upload failed. Please try again.';
      setError(errorMessage);
    } finally {
      setUploading(false);
      setUploadProgress(0);
    }
  };

  return (
    <Paper className="upload-section" style={{ padding: '24px', marginBottom: '30px' }}>
      <h2 className="section-title">Upload CSV Data</h2>

      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}

      <div
        className={`upload-zone ${dragging ? 'dragging' : ''}`}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onClick={() => fileInputRef.current?.click()}
      >
        <CloudUploadIcon style={{ fontSize: 64, color: '#667eea', marginBottom: 16 }} />
        <Typography variant="h6" gutterBottom>
          {file ? file.name : 'Drop CSV file here or click to browse'}
        </Typography>
        <Typography variant="body2" color="textSecondary">
          CSV file with Equipment_Name, Type, Flowrate, Pressure, Temperature columns
        </Typography>
        <Typography variant="caption" color="textSecondary" style={{ marginTop: 8 }}>
          Maximum file size: 5MB
        </Typography>

        <input
          ref={fileInputRef}
          type="file"
          accept=".csv"
          onChange={handleFileInputChange}
          style={{ display: 'none' }}
        />
      </div>

      {uploading && (
        <div style={{ marginTop: 20 }}>
          <LinearProgress variant="determinate" value={uploadProgress} />
          <Typography variant="body2" align="center" style={{ marginTop: 8 }}>
            Uploading... {uploadProgress}%
          </Typography>
        </div>
      )}

      {file && !uploading && (
        <div style={{ marginTop: 20, display: 'flex', gap: 12 }}>
          <Button
            variant="contained"
            color="primary"
            onClick={handleUpload}
            fullWidth
            style={{ textTransform: 'none', padding: '12px' }}
          >
            Upload and Process
          </Button>
          <Button
            variant="outlined"
            onClick={() => {
              setFile(null);
              if (fileInputRef.current) {
                fileInputRef.current.value = '';
              }
            }}
            style={{ textTransform: 'none', padding: '12px' }}
          >
            Clear
          </Button>
        </div>
      )}
    </Paper>
  );
}

export default UploadSection;