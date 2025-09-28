/**
 * Application Configuration
 * Centralizes all configuration settings for the application
 */

// Load environment variables
const dotenv = require('dotenv');
dotenv.config();

// Export configuration object
module.exports = {
  // Server configuration
  server: {
    port: process.env.PORT || 3000,
    environment: process.env.NODE_ENV || 'development'
  },

  // Cors configuration
  cors: {
    origin: process.env.CORS_ORIGIN || '*',
    methods: ['GET', 'POST', 'PUT', 'DELETE'],
    credentials: true
  },

  // API configuration
  api: {
    prefix: '/api',
    version: 'v1'
  },

  // Logging configuration
  logging: {
    level: process.env.LOG_LEVEL || 'dev'
  }
};