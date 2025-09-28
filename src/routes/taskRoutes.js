const express = require('express');
const router = express.Router();

// Import task model (placeholder for now)
const Task = require('../models/taskModel');

/**
 * @route   GET /api/tasks
 * @desc    Get all tasks
 * @access  Public
 */
router.get('/', async (req, res) => {
  try {
    // Placeholder for database query
    const tasks = []; // This will be replaced with actual data from the database
    res.status(200).json({
      success: true,
      count: tasks.length,
      data: tasks
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Server Error'
    });
  }
});

/**
 * @route   GET /api/tasks/:id
 * @desc    Get single task
 * @access  Public
 */
router.get('/:id', async (req, res) => {
  try {
    // Placeholder for database query
    const task = null; // This will be replaced with actual data from the database

    if (!task) {
      return res.status(404).json({
        success: false,
        error: 'Task not found'
      });
    }

    res.status(200).json({
      success: true,
      data: task
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Server Error'
    });
  }
});

/**
 * @route   POST /api/tasks
 * @desc    Create a task
 * @access  Public
 */
router.post('/', async (req, res) => {
  try {
    // Validate request
    const { title, description, status } = req.body;

    if (!title) {
      return res.status(400).json({
        success: false,
        error: 'Please provide a title for the task'
      });
    }

    // Placeholder for database insertion
    const task = {
      id: Date.now().toString(),
      title,
      description: description || '',
      status: status || 'pending',
      createdAt: new Date().toISOString()
    };

    res.status(201).json({
      success: true,
      data: task
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Server Error'
    });
  }
});

/**
 * @route   PUT /api/tasks/:id
 * @desc    Update a task
 * @access  Public
 */
router.put('/:id', async (req, res) => {
  try {
    // Validate request
    const { title, description, status } = req.body;

    // Placeholder for database update
    const taskId = req.params.id;
    const task = {
      id: taskId,
      title,
      description,
      status,
      updatedAt: new Date().toISOString()
    };

    if (!task) {
      return res.status(404).json({
        success: false,
        error: 'Task not found'
      });
    }

    res.status(200).json({
      success: true,
      data: task
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Server Error'
    });
  }
});

/**
 * @route   DELETE /api/tasks/:id
 * @desc    Delete a task
 * @access  Public
 */
router.delete('/:id', async (req, res) => {
  try {
    // Placeholder for database deletion
    const taskId = req.params.id;

    // Pretend we've deleted it
    const success = true;

    if (!success) {
      return res.status(404).json({
        success: false,
        error: 'Task not found'
      });
    }

    res.status(200).json({
      success: true,
      data: {}
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: 'Server Error'
    });
  }
});

module.exports = router;