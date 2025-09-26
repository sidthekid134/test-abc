/**
 * Database connection configuration
 */
const mongoose = require('mongoose');

/**
 * Connect to MongoDB
 * @returns {Promise} Mongoose connection promise
 */
const connectDB = async () => {
  try {
    // Get connection string based on environment
    const connectionString =
      process.env.NODE_ENV === 'test'
        ? process.env.MONGODB_URI_TEST
        : process.env.MONGODB_URI;

    if (!connectionString) {
      throw new Error('MongoDB connection string not found in environment variables');
    }

    // Connect to MongoDB with improved settings
    const conn = await mongoose.connect(connectionString, {
      serverSelectionTimeoutMS: 5000 // Timeout after 5 seconds instead of 30
    });

    console.log(`MongoDB connected: ${conn.connection.host}`);
    return conn;
  } catch (error) {
    console.error(`Error connecting to MongoDB: ${error.message}`);
    // Don't exit the process, let the application handle the error
    throw error;
  }
};

/**
 * Disconnect from MongoDB (useful for tests)
 * @returns {Promise} Mongoose disconnection promise
 */
const disconnectDB = async () => {
  try {
    await mongoose.disconnect();
    console.log('MongoDB disconnected');
  } catch (error) {
    console.error(`Error disconnecting from MongoDB: ${error.message}`);
    throw error;
  }
};

module.exports = { connectDB, disconnectDB };