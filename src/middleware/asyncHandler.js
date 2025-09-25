/**
 * Async handler to avoid try/catch blocks in route handlers
 * Wraps async functions to automatically catch errors and pass to next()
 * 
 * @param {Function} fn - Async function to wrap
 * @returns {Function} Express middleware function
 */
const asyncHandler = (fn) => {
  return (req, res, next) => {
    Promise.resolve(fn(req, res, next)).catch(next);
  };
};

module.exports = asyncHandler;