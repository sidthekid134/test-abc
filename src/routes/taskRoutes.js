const express = require('express');
const taskController = require('../controllers/taskController');

const router = express.Router();

/**
 * @route   GET /api/tasks
 * @desc    Get all tasks
 * @access  Public
 */
router.get('/', taskController.getAllTasks);

/**
 * @route   GET /api/tasks/:id
 * @desc    Get a specific task by ID
 * @access  Public
 */
router.get('/:id', taskController.getTaskById);

/**
 * @route   POST /api/tasks
 * @desc    Create a new task
 * @access  Public
 */
router.post('/', taskController.createTask);

/**
 * @route   PUT /api/tasks/:id
 * @desc    Update an existing task
 * @access  Public
 */
router.put('/:id', taskController.updateTask);

/**
 * @route   DELETE /api/tasks/:id
 * @desc    Delete a task
 * @access  Public
 */
router.delete('/:id', taskController.deleteTask);

module.exports = router;