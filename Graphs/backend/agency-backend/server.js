const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

const statesRouter = require('./routes/states');
const countiesRouter = require('./routes/counties');
const statusRouter = require('./routes/status');
const agenciesRouter = require('./routes/agencies');

app.use('/api/states', statesRouter);
app.use('/api/counties', countiesRouter);
app.use('/api/status', statusRouter);
app.use('/api/agencies', agenciesRouter);

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
