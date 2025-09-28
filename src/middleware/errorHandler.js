/**
 * Error Handler Middleware
 * Centralized error handling for the application
 */

// Error response helper
const errorResponse = (res, statusCode, message, errors = null) => {
  const response = {
    success: false,
    error: message
  };

  if (errors) {
    response.errors = errors;
  }

  return res.status(statusCode).json(response);
};

// Custom error class for API errors
class APIError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }
}

// Custom error classes for specific error types
class NotFoundError extends APIError {
  constructor(message = 'Resource not found') {
    super(message, 404);
  }
}

class BadRequestError extends APIError {
  constructor(message = 'Bad request') {
    super(message, 400);
  }
}

class UnauthorizedError extends APIError {
  constructor(message = 'Unauthorized') {
    super(message, 401);
  }
}

class ForbiddenError extends APIError {
  constructor(message = 'Forbidden') {
    super(message, 403);
  }
}

// Main error handler middleware
const errorHandler = (err, req, res, next) => {
  let error = { ...err };
  error.message = err.message;

  // Log error for debugging
  console.error(err);

  // Mongoose validation error
  if (err.name === 'ValidationError') {
    const message = 'Validation Error';
    const errors = Object.values(err.errors).map(val => val.message);
    return errorResponse(res, 400, message, errors);
  }

  // Mongoose duplicate key error
  if (err.code === 11000) {
    const message = 'Duplicate field value entered';
    return errorResponse(res, 400, message);
  }

  // Mongoose bad ObjectId
  if (err.name === 'CastError') {
    const message = `Resource not found with id of ${err.value}`;
    return errorResponse(res, 404, message);
  }

  // JSON parse error
  if (err instanceof SyntaxError && err.status === 400 && 'body' in err) {
    return errorResponse(res, 400, 'Invalid JSON payload');
  }

  // Custom API errors
  if (err instanceof APIError) {
    return errorResponse(res, err.statusCode, err.message);
  }

  // Default to 500 server error
  return errorResponse(
    res,
    error.statusCode || 500,
    error.message || 'Server Error'
  );
};

module.exports = {
  errorHandler,
  APIError,
  NotFoundError,
  BadRequestError,
  UnauthorizedError,
  ForbiddenError
};