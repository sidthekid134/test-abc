const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const dotenv = require('dotenv');

// Load environment variables
dotenv.config();

// Import routes
const taskRoutes = require('./src/routes/taskRoutes');

// Import middleware
const errorHandler = require('./src/middleware/errorHandler');
const notFound = require('./src/middleware/notFound');

// Initialize express app
const app = express();

// Define port
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(morgan('dev'));

// Routes
app.use('/api/tasks', taskRoutes);

// Root route
app.get('/', (req, res) => {
  res.json({
    message: 'Welcome to Task Management API'
  });
});

// Not found middleware (handle 404 errors)
app.use(notFound);

// Error handling middleware (handle all other errors)
app.use(errorHandler);

// Start server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

module.exports = app;