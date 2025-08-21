const express = require('express');
const router = express.Router();
const pool = require('../db');

router.get('/', async (req, res) => {
  const { state_id } = req.query;
  try {
    let result;
    if (state_id) {
      result = await pool.query('SELECT * FROM counties WHERE state_id=$1 ORDER BY county_id;', [state_id]);
    } else {
      result = await pool.query('SELECT * FROM counties ORDER BY county_id;');
    }
    res.json(result.rows);
  } catch (err) {
    console.error(err);
    res.status(500).send('Server error');
  }
});

module.exports = router;
