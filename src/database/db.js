/**
 * Database Connection Module
 * Handles connection to MongoDB using Mongoose
 */

const mongoose = require('mongoose');
const config = require('../config/config');

// Connect to MongoDB
const connectDB = async () => {
  try {
    const conn = await mongoose.connect(config.database.url, config.database.options);
    console.log(`MongoDB Connected: ${conn.connection.host}`);
    return conn;
  } catch (error) {
    console.error(`Error connecting to MongoDB: ${error.message}`);
    process.exit(1);
  }
};

module.exports = { connectDB };