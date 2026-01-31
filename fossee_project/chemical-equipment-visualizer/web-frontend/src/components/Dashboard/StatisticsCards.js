/**
 * Statistics Cards Component
 */

import React from 'react';
import { Paper, Typography } from '@mui/material';
import {
  Assessment as AssessmentIcon,
  Speed as SpeedIcon,
  Compress as PressureIcon,
  Thermostat as TempIcon,
} from '@mui/icons-material';

function StatisticsCards({ statistics }) {
  if (!statistics) return null;

  const stats = [
    {
      label: 'Total Equipment',
      value: statistics.total_equipment || 0,
      icon: <AssessmentIcon />,
      color: '#667eea',
      bgColor: '#e8ebff',
    },
    {
      label: 'Avg Flowrate',
      value: statistics.avg_flowrate ? statistics.avg_flowrate.toFixed(2) : 'N/A',
      icon: <SpeedIcon />,
      color: '#2ecc71',
      bgColor: '#e5f7ed',
    },
    {
      label: 'Avg Pressure',
      value: statistics.avg_pressure ? statistics.avg_pressure.toFixed(2) : 'N/A',
      icon: <PressureIcon />,
      color: '#f39c12',
      bgColor: '#fff5e6',
    },
    {
      label: 'Avg Temperature',
      value: statistics.avg_temperature ? statistics.avg_temperature.toFixed(2) : 'N/A',
      icon: <TempIcon />,
      color: '#e74c3c',
      bgColor: '#ffe5e5',
    },
  ];

  return (
    <div className="stats-grid">
      {stats.map((stat, index) => (
        <Paper key={index} className="stat-card">
          <div className="stat-icon" style={{ backgroundColor: stat.bgColor, color: stat.color }}>
            {stat.icon}
          </div>
          <div className="stat-value">{stat.value}</div>
          <div className="stat-label">{stat.label}</div>
        </Paper>
      ))}
    </div>
  );
}

export default StatisticsCards;