/**
 * Dataset History Component
 */

import React from 'react';
import {
  Paper,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Chip,
  Tooltip,
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import PictureAsPdfIcon from '@mui/icons-material/PictureAsPdf';
import VisibilityIcon from '@mui/icons-material/Visibility';

function DatasetHistory({
  datasets,
  currentDataset,
  onDatasetSelect,
  onDatasetDelete,
  onDownloadPDF,
}) {
  if (!datasets || datasets.length === 0) {
    return null;
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
  };

  return (
    <Paper style={{ padding: '24px', marginBottom: '30px' }}>
      <h2 className="section-title">Recent Datasets (Last 5)</h2>
      
      <List>
        {datasets.map((dataset) => (
          <ListItem
            key={dataset.id}
            style={{
              backgroundColor:
                currentDataset && currentDataset.id === dataset.id
                  ? '#e8ebff'
                  : 'white',
              marginBottom: '8px',
              borderRadius: '8px',
              border: '1px solid #e0e0e0',
            }}
          >
            <ListItemText
              primary={
                <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                  <strong>{dataset.name}</strong>
                  {currentDataset && currentDataset.id === dataset.id && (
                    <Chip label="Active" size="small" color="primary" />
                  )}
                </div>
              }
              secondary={
                <>
                  <div>Uploaded: {formatDate(dataset.uploaded_at)}</div>
                  <div>Equipment: {dataset.total_equipment} items</div>
                </>
              }
            />
            <ListItemSecondaryAction>
              <Tooltip title="View Dataset">
                <IconButton
                  edge="end"
                  onClick={() => onDatasetSelect(dataset.id)}
                  color="primary"
                  style={{ marginRight: 8 }}
                >
                  <VisibilityIcon />
                </IconButton>
              </Tooltip>
              
              <Tooltip title="Download PDF Report">
                <IconButton
                  edge="end"
                  onClick={() => onDownloadPDF(dataset.id)}
                  color="success"
                  style={{ marginRight: 8 }}
                >
                  <PictureAsPdfIcon />
                </IconButton>
              </Tooltip>
              
              <Tooltip title="Delete Dataset">
                <IconButton
                  edge="end"
                  onClick={() => {
                    if (window.confirm('Are you sure you want to delete this dataset?')) {
                      onDatasetDelete(dataset.id);
                    }
                  }}
                  color="error"
                >
                  <DeleteIcon />
                </IconButton>
              </Tooltip>
            </ListItemSecondaryAction>
          </ListItem>
        ))}
      </List>
    </Paper>
  );
}

export default DatasetHistory;