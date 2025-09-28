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

  // Database configuration
  mongoURI: process.env.MONGO_URI || 'mongodb://localhost:27017/task-management',
  mongoOptions: {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  }

  // Future configurations to be added:
  // - Authentication (JWT, etc.)
  // - Logging
};