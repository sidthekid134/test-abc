/**
 * Application Configuration
 */
const dotenv = require('dotenv');

// Load environment variables
dotenv.config();

module.exports = {
  // Server configuration
  port: process.env.PORT || 3000,
  nodeEnv: process.env.NODE_ENV || 'development',

  // Future configurations to be added:
  // - Database connection
  // - Authentication (JWT, etc.)
  // - Logging
};