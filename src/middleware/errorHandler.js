/**
 * Global error handling middleware
 * Standardizes error responses across the API
 */

const errorHandler = (err, req, res, next) => {
  // Log error for server debugging
  console.error('Error:', err);

  // Default error status and message
  let statusCode = err.statusCode || 500;
  let message = err.message || 'Internal Server Error';
  let errorDetails = null;

  // Mongoose validation error
  if (err.name === 'ValidationError') {
    statusCode = 400;
    message = 'Validation Error';
    errorDetails = {};
    
    // Extract validation error messages
    for (const field in err.errors) {
      errorDetails[field] = err.errors[field].message;
    }
    
    return res.status(statusCode).json({
      success: false,
      message,
      errors: errorDetails,
      requestId: req.id // For tracking purposes if using request ID middleware
    });
  }

  // Mongoose CastError (invalid ID)
  if (err.name === 'CastError') {
    statusCode = 400;
    message = `Invalid ${err.path}: ${err.value}`;
    errorDetails = {
      path: err.path,
      value: err.value
    };
  }

  // Mongoose duplicate key error
  if (err.code === 11000) {
    statusCode = 400;
    message = `Duplicate field value entered`;
    errorDetails = err.keyValue;
  }

  // SyntaxError (usually invalid JSON)
  if (err instanceof SyntaxError && err.status === 400 && 'body' in err) {
    statusCode = 400;
    message = 'Invalid request body format - JSON parsing error';
  }
  
  // Handle JWT errors
  if (err.name === 'JsonWebTokenError') {
    statusCode = 401;
    message = 'Invalid token';
  }

  if (err.name === 'TokenExpiredError') {
    statusCode = 401;
    message = 'Token expired';
  }

  // Return standardized error response
  res.status(statusCode).json({
    success: false,
    message,
    errors: errorDetails,
    stack: process.env.NODE_ENV === 'development' ? err.stack : undefined,
    requestId: req.id // For tracking purposes if using request ID middleware
  });
};

module.exports = errorHandler;