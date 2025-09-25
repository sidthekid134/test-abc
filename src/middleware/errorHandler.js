/**
 * Global error handling middleware
 * Standardizes error responses across the API
 */

const errorHandler = (err, req, res, next) => {
  // Default error status and message
  let statusCode = err.statusCode || 500;
  let message = err.message || 'Internal Server Error';

  // Mongoose validation error
  if (err.name === 'ValidationError') {
    statusCode = 400;
    const validationErrors = {};
    
    // Extract validation error messages
    for (const field in err.errors) {
      validationErrors[field] = err.errors[field].message;
    }
    
    return res.status(statusCode).json({
      success: false,
      message: 'Validation Error',
      errors: validationErrors
    });
  }

  // Mongoose CastError (invalid ID)
  if (err.name === 'CastError') {
    statusCode = 400;
    message = `Invalid ${err.path}: ${err.value}`;
  }

  // Mongoose duplicate key error
  if (err.code === 11000) {
    statusCode = 400;
    message = `Duplicate field value entered for ${Object.keys(err.keyValue)}`;
  }

  // Return standardized error response
  res.status(statusCode).json({
    success: false,
    message,
    error: process.env.NODE_ENV === 'development' ? err.stack : undefined
  });
};

module.exports = errorHandler;