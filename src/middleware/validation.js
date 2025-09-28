/**
 * Validation Middleware
 * Contains validation rules for API endpoints
 */

const { body, param, query, validationResult } = require('express-validator');

// Utility function to check for validation errors
exports.checkValidation = (req, res, next) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({
      success: false,
      errors: errors.array().map(error => error.msg)
    });
  }
  next();
};

// Task validation rules
exports.taskValidationRules = {
  create: [
    body('title')
      .trim()
      .notEmpty().withMessage('Title is required')
      .isLength({ max: 100 }).withMessage('Title cannot be more than 100 characters'),
    body('description')
      .optional()
      .trim(),
    body('status')
      .optional()
      .isIn(['pending', 'in_progress', 'completed']).withMessage('Status must be one of: pending, in_progress, completed'),
    body('priority')
      .optional()
      .isIn(['low', 'medium', 'high']).withMessage('Priority must be one of: low, medium, high'),
    body('dueDate')
      .optional()
      .isISO8601().withMessage('Due date must be a valid date'),
    body('tags')
      .optional()
      .isArray().withMessage('Tags must be an array')
  ],

  update: [
    param('id')
      .isMongoId().withMessage('Invalid task ID format'),
    body('title')
      .optional()
      .trim()
      .notEmpty().withMessage('Title cannot be empty')
      .isLength({ max: 100 }).withMessage('Title cannot be more than 100 characters'),
    body('description')
      .optional()
      .trim(),
    body('status')
      .optional()
      .isIn(['pending', 'in_progress', 'completed']).withMessage('Status must be one of: pending, in_progress, completed'),
    body('priority')
      .optional()
      .isIn(['low', 'medium', 'high']).withMessage('Priority must be one of: low, medium, high'),
    body('dueDate')
      .optional()
      .isISO8601().withMessage('Due date must be a valid date'),
    body('tags')
      .optional()
      .isArray().withMessage('Tags must be an array')
  ],

  getById: [
    param('id')
      .isMongoId().withMessage('Invalid task ID format')
  ],

  delete: [
    param('id')
      .isMongoId().withMessage('Invalid task ID format')
  ],

  list: [
    query('page')
      .optional()
      .isInt({ min: 1 }).withMessage('Page must be a positive integer'),
    query('limit')
      .optional()
      .isInt({ min: 1, max: 100 }).withMessage('Limit must be between 1 and 100'),
    query('sort')
      .optional()
      .isString().withMessage('Sort must be a string'),
    query('status')
      .optional()
      .isIn(['pending', 'in_progress', 'completed']).withMessage('Status must be one of: pending, in_progress, completed'),
    query('priority')
      .optional()
      .isIn(['low', 'medium', 'high']).withMessage('Priority must be one of: low, medium, high')
  ]
};