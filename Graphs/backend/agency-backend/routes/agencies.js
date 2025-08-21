const express = require('express');
const router = express.Router();
const pool = require('../db');

router.get('/', async (req, res) => {
  const { state_id, county_id, status_id } = req.query; // Added status_id here
  
  // Debug logging
  console.log('API received filters:', { state_id, county_id, status_id });
  
  try {
    let query = `
      SELECT a.*, 
             s.state_id, s.state_name, 
             c.county_id, c.county_name, 
             st.status_id, st.status_name
      FROM agencies a
      LEFT JOIN counties c ON a.county_id = c.county_id
      LEFT JOIN states s ON c.state_id = s.state_id
      LEFT JOIN status st ON a.status_id = st.status_id
    `;
    const params = [];
    const conditions = [];
    
    if (state_id) {
      conditions.push(`s.state_id = $${params.length + 1}`);
      params.push(state_id);
    }
    
    if (county_id) {
      conditions.push(`c.county_id = $${params.length + 1}`);
      params.push(county_id);
    }
    
    // Added status_id filter
    if (status_id) {
      conditions.push(`st.status_id = $${params.length + 1}`);
      params.push(status_id);
    }
    
    if (conditions.length) {
      query += ' WHERE ' + conditions.join(' AND ');
    }

    query += ' ORDER BY a.agency_id;';

    // Debug logging
    console.log('Final SQL query:', query);
    console.log('Query parameters:', params);

    const result = await pool.query(query, params);

    // Transform result to nested objects
    const formatted = result.rows.map(row => ({
      id: row.agency_id, // Make sure this matches your frontend expectation
      agency_id: row.agency_id,
      agency_name: row.agency_name,
      type: row.type,
      support_type: row.support_type,
      signed: row.signed,
      last_seen: row.last_seen,
      extracted_link: row.extracted_link,
      county: {
        county_id: row.county_id,
        county_name: row.county_name
      },
      state: {
        state_id: row.state_id,
        state_name: row.state_name
      },
      status: {
        status_id: row.status_id,
        status_name: row.status_name
      }
    }));

    console.log(`Returning ${formatted.length} agencies after filtering`);
    res.json(formatted);
  } catch (err) {
    console.error('Database error:', err);
    res.status(500).json({ error: 'Server error', details: err.message });
  }
});

module.exports = router;