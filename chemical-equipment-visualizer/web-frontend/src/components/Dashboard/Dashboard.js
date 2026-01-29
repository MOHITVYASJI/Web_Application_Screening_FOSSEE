/**
 * Main Dashboard Component
 */

import React, { useState, useEffect } from 'react';
import { Button, AppBar, Toolbar, Typography } from '@mui/material';
import LogoutIcon from '@mui/icons-material/Logout';
import { authAPI, datasetAPI } from '../../services/api';

import UploadSection from './UploadSection';
import StatisticsCards from './StatisticsCards';
import ChartsSection from './ChartsSection';
import DataTable from './DataTable';
import DatasetHistory from './DatasetHistory';

function Dashboard({ onLogout }) {
  const [user, setUser] = useState(authAPI.getUser());
  const [datasets, setDatasets] = useState([]);
  const [currentDataset, setCurrentDataset] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadDatasets();
  }, []);

  const loadDatasets = async () => {
    setLoading(true);
    try {
      const data = await datasetAPI.getDatasets();
      setDatasets(data.results || []);
      
      // Set first dataset as current if available
      if (data.results && data.results.length > 0 && !currentDataset) {
        loadDatasetDetails(data.results[0].id);
      }
    } catch (err) {
      setError('Failed to load datasets');
    } finally {
      setLoading(false);
    }
  };

  const loadDatasetDetails = async (id) => {
    setLoading(true);
    try {
      const data = await datasetAPI.getDataset(id);
      setCurrentDataset(data);
    } catch (err) {
      setError('Failed to load dataset details');
    } finally {
      setLoading(false);
    }
  };

  const handleUploadSuccess = (uploadedDataset) => {
    // Reload datasets to get updated list
    loadDatasets();
    // Set the newly uploaded dataset as current
    setCurrentDataset(uploadedDataset.dataset);
  };

  const handleDatasetSelect = (id) => {
    loadDatasetDetails(id);
  };

  const handleDatasetDelete = async (id) => {
    try {
      await datasetAPI.deleteDataset(id);
      
      // Reload datasets
      await loadDatasets();
      
      // Clear current dataset if it was deleted
      if (currentDataset && currentDataset.id === id) {
        setCurrentDataset(null);
      }
    } catch (err) {
      setError('Failed to delete dataset');
    }
  };

  const handleDownloadPDF = async (id) => {
    try {
      await datasetAPI.downloadPDF(id, `equipment_report_${id}.pdf`);
    } catch (err) {
      setError('Failed to download PDF');
    }
  };

  return (
    <div className="dashboard">
      <AppBar position="static" elevation={1}>
        <Toolbar className="dashboard-header" style={{ background: 'white' }}>
          <div>
            <Typography variant="h5" component="h1" style={{ color: '#2c3e50', fontWeight: 700 }}>
              Chemical Equipment Visualizer
            </Typography>
            <Typography variant="body2" style={{ color: '#7f8c8d' }}>
              Welcome, {user?.username || 'User'}
            </Typography>
          </div>
          <Button
            variant="outlined"
            startIcon={<LogoutIcon />}
            onClick={onLogout}
            style={{ textTransform: 'none' }}
          >
            Logout
          </Button>
        </Toolbar>
      </AppBar>

      <div className="dashboard-content">
        {error && <div className="error-message">{error}</div>}

        {/* Upload Section */}
        <UploadSection onUploadSuccess={handleUploadSuccess} />

        {/* Dataset History */}
        {datasets.length > 0 && (
          <DatasetHistory
            datasets={datasets}
            currentDataset={currentDataset}
            onDatasetSelect={handleDatasetSelect}
            onDatasetDelete={handleDatasetDelete}
            onDownloadPDF={handleDownloadPDF}
          />
        )}

        {/* Statistics and Visualizations */}
        {currentDataset && (
          <>
            <h2 className="section-title">Dataset: {currentDataset.name}</h2>
            
            <StatisticsCards statistics={currentDataset.statistics} />
            
            <ChartsSection
              statistics={currentDataset.statistics}
              data={currentDataset.data_json}
            />
            
            <DataTable data={currentDataset.data_json} />
          </>
        )}

        {!currentDataset && datasets.length === 0 && !loading && (
          <div className="empty-state">
            <div className="empty-state-icon">📁</div>
            <h3>No Datasets Yet</h3>
            <p>Upload a CSV file to get started with data visualization</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;