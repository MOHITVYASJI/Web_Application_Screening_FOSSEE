/**
 * Charts Section Component with Chart.js
 */

import React from 'react';
import { Paper, Grid } from '@mui/material';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
  LineElement,
} from 'chart.js';
import { Bar, Pie, Line } from 'react-chartjs-2';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
  LineElement
);

function ChartsSection({ statistics, data }) {
  if (!statistics || !data) return null;

  // Equipment Distribution Bar Chart
  const distributionData = {
    labels: Object.keys(statistics.equipment_distribution || {}),
    datasets: [
      {
        label: 'Equipment Count',
        data: Object.values(statistics.equipment_distribution || {}),
        backgroundColor: 'rgba(102, 126, 234, 0.8)',
        borderColor: 'rgba(102, 126, 234, 1)',
        borderWidth: 1,
      },
    ],
  };

  const barOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Equipment Type Distribution',
        font: {
          size: 16,
          weight: 'bold',
        },
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 1,
        },
      },
    },
  };

  // Equipment Distribution Pie Chart
  const pieData = {
    labels: Object.keys(statistics.equipment_distribution || {}),
    datasets: [
      {
        data: Object.values(statistics.equipment_distribution || {}),
        backgroundColor: [
          '#667eea',
          '#2ecc71',
          '#f39c12',
          '#e74c3c',
          '#9b59b6',
          '#3498db',
          '#1abc9c',
          '#e67e22',
        ],
        borderWidth: 2,
        borderColor: '#fff',
      },
    ],
  };

  const pieOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'right',
      },
      title: {
        display: true,
        text: 'Equipment Distribution (Pie Chart)',
        font: {
          size: 16,
          weight: 'bold',
        },
      },
    },
  };

  // Parameter Trends Line Chart
  const parametersData = {
    labels: data.slice(0, 20).map((item) => item.Equipment_Name),
    datasets: [
      {
        label: 'Flowrate',
        data: data.slice(0, 20).map((item) => item.Flowrate),
        borderColor: 'rgb(102, 126, 234)',
        backgroundColor: 'rgba(102, 126, 234, 0.2)',
        tension: 0.4,
      },
      {
        label: 'Pressure',
        data: data.slice(0, 20).map((item) => item.Pressure),
        borderColor: 'rgb(46, 204, 113)',
        backgroundColor: 'rgba(46, 204, 113, 0.2)',
        tension: 0.4,
      },
      {
        label: 'Temperature',
        data: data.slice(0, 20).map((item) => item.Temperature),
        borderColor: 'rgb(231, 76, 60)',
        backgroundColor: 'rgba(231, 76, 60, 0.2)',
        tension: 0.4,
      },
    ],
  };

  const lineOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Parameter Trends (First 20 Equipment)',
        font: {
          size: 16,
          weight: 'bold',
        },
      },
    },
    scales: {
      y: {
        beginAtZero: false,
      },
    },
  };

  return (
    <div style={{ marginBottom: 30 }}>
      <h2 className="section-title">Data Visualizations</h2>
      
      <Grid container spacing={3}>
        {/* Bar Chart */}
        <Grid item xs={12} md={6}>
          <Paper className="chart-container">
            <div style={{ height: 350 }}>
              <Bar data={distributionData} options={barOptions} />
            </div>
          </Paper>
        </Grid>

        {/* Pie Chart */}
        <Grid item xs={12} md={6}>
          <Paper className="chart-container">
            <div style={{ height: 350 }}>
              <Pie data={pieData} options={pieOptions} />
            </div>
          </Paper>
        </Grid>

        {/* Line Chart */}
        <Grid item xs={12}>
          <Paper className="chart-container">
            <div style={{ height: 400 }}>
              <Line data={parametersData} options={lineOptions} />
            </div>
          </Paper>
        </Grid>
      </Grid>
    </div>
  );
}

export default ChartsSection;