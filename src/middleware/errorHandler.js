/**
 * Error handling middleware
 */

// Handle 404 errors
const notFound = (req, res, next) => {
  const error = new Error(`Not Found - ${req.originalUrl}`);
  error.status = 404;
  next(error);
};

// Handle all other errors
const errorHandler = (err, req, res, next) => {
  const statusCode = err.status || 500;
  const errorResponse = {
    message: err.message,
    stack: process.env.NODE_ENV === 'production' ? '🥞' : err.stack,
  };

  if (process.env.NODE_ENV !== 'production') {
    console.error(`[Error] ${err.message}`, err.stack);
  }

  res.status(statusCode).json({
    success: false,
    error: errorResponse,
    timestamp: new Date().toISOString(),
  });
};

module.exports = {
  notFound,
  errorHandler,
};