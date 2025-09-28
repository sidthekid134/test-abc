const express = require('express');
const router = express.Router();

// Import task controller
const taskController = require('../controllers/taskController');

// Import validation middleware
const { taskValidationRules, checkValidation } = require('../middleware/validation');

/**
 * @route   GET /api/v2/tasks
 * @desc    Get all tasks with filtering, pagination and sorting
 * @access  Public
 */
router.get(
  '/',
  taskValidationRules.list,
  checkValidation,
  taskController.getTasks
);

/**
 * @route   GET /api/v2/tasks/:id
 * @desc    Get single task by ID
 * @access  Public
 */
router.get(
  '/:id',
  taskValidationRules.getById,
  checkValidation,
  taskController.getTaskById
);

/**
 * @route   POST /api/v2/tasks
 * @desc    Create a new task
 * @access  Public
 */
router.post(
  '/',
  taskValidationRules.create,
  checkValidation,
  taskController.createTask
);

/**
 * @route   PUT /api/v2/tasks/:id
 * @desc    Update a task by ID
 * @access  Public
 */
router.put(
  '/:id',
  taskValidationRules.update,
  checkValidation,
  taskController.updateTask
);

/**
 * @route   DELETE /api/v2/tasks/:id
 * @desc    Delete a task by ID
 * @access  Public
 */
router.delete(
  '/:id',
  taskValidationRules.delete,
  checkValidation,
  taskController.deleteTask
);

module.exports = router;