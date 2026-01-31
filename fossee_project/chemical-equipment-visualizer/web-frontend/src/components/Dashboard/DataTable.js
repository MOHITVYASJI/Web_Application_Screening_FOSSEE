/**
 * Data Table Component
 */

import React, { useState } from 'react';
import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
} from '@mui/material';

function DataTable({ data }) {
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);

  if (!data || data.length === 0) {
    return null;
  }

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const paginatedData = data.slice(
    page * rowsPerPage,
    page * rowsPerPage + rowsPerPage
  );

  return (
    <div className="data-table-container">
      <h2 className="section-title">Equipment Data</h2>
      
      <TableContainer>
        <Table>
          <TableHead>
            <TableRow style={{ backgroundColor: '#667eea' }}>
              <TableCell style={{ color: 'white', fontWeight: 'bold' }}>
                Equipment Name
              </TableCell>
              <TableCell style={{ color: 'white', fontWeight: 'bold' }}>
                Type
              </TableCell>
              <TableCell align="right" style={{ color: 'white', fontWeight: 'bold' }}>
                Flowrate
              </TableCell>
              <TableCell align="right" style={{ color: 'white', fontWeight: 'bold' }}>
                Pressure
              </TableCell>
              <TableCell align="right" style={{ color: 'white', fontWeight: 'bold' }}>
                Temperature
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {paginatedData.map((row, index) => (
              <TableRow
                key={index}
                sx={{
                  '&:nth-of-type(odd)': { backgroundColor: '#f9f9f9' },
                  '&:hover': { backgroundColor: '#f0f2ff' },
                }}
              >
                <TableCell>{row.Equipment_Name}</TableCell>
                <TableCell>{row.Type}</TableCell>
                <TableCell align="right">{row.Flowrate?.toFixed(2)}</TableCell>
                <TableCell align="right">{row.Pressure?.toFixed(2)}</TableCell>
                <TableCell align="right">{row.Temperature?.toFixed(2)}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <TablePagination
        rowsPerPageOptions={[5, 10, 25, 50]}
        component="div"
        count={data.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
      />
    </div>
  );
}

export default DataTable;