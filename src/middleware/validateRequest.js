/**
 * Middleware for validating request data
 * @param {Object} schema - Validation schema object
 * @returns {Function} Express middleware function
 */
const validateRequest = (schema) => {
  return (req, res, next) => {
    // Only validate body if schema is provided and request has a body
    if (schema && req.body) {
      // Extract allowed fields from schema
      const allowedFields = Object.keys(schema);
      
      // Check for unknown fields
      const unknownFields = Object.keys(req.body).filter(
        field => !allowedFields.includes(field)
      );
      
      if (unknownFields.length > 0) {
        return res.status(400).json({
          success: false,
          message: `Unknown field(s): ${unknownFields.join(', ')}`,
          error: 'Validation Error'
        });
      }
      
      // Validate required fields
      for (const [field, rules] of Object.entries(schema)) {
        // Skip if not required
        if (!rules.required) continue;
        
        if (rules.required && (req.body[field] === undefined || req.body[field] === null || req.body[field] === '')) {
          return res.status(400).json({
            success: false,
            message: `${field} is required`,
            error: 'Validation Error'
          });
        }
      }
    }
    
    next();
  };
};

module.exports = validateRequest;