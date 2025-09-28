const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const config = require('./src/config/config');

// Initialize express app
const app = express();
const PORT = config.server.port;

// Middleware
app.use(cors(config.cors));
app.use(express.json());
app.use(morgan(config.logging.level));

// Import routes
const taskRoutes = require('./src/routes/taskRoutes');

// Use routes
app.use(`${config.api.prefix}/tasks`, taskRoutes);

// Root route
app.get('/', (req, res) => {
  res.json({ message: 'Welcome to Apollo Task Management API' });
});

// Start server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT} in ${config.server.environment} mode`);
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    success: false,
    error: 'Server Error'
  });
});

module.exports = app;