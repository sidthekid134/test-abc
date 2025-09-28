const express = require('express');
const router = express.Router();

// Import task model (to be implemented later)
const Task = require('../models/task');

/**
 * @route   GET /api/tasks
 * @desc    Get all tasks
 * @access  Public
 */
router.get('/', async (req, res) => {
  try {
    // Mock response for now, will be replaced with actual data later
    res.json({
      success: true,
      data: [
        { id: 1, title: 'Task 1', description: 'Description for Task 1', completed: false, createdAt: new Date() },
        { id: 2, title: 'Task 2', description: 'Description for Task 2', completed: true, createdAt: new Date() }
      ]
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

/**
 * @route   GET /api/tasks/:id
 * @desc    Get task by ID
 * @access  Public
 */
router.get('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    // Mock response for now, will be replaced with actual data later
    res.json({
      success: true,
      data: { id: parseInt(id), title: `Task ${id}`, description: `Description for Task ${id}`, completed: false, createdAt: new Date() }
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

/**
 * @route   POST /api/tasks
 * @desc    Create a new task
 * @access  Public
 */
router.post('/', async (req, res) => {
  try {
    const { title, description } = req.body;

    // Validate request
    if (!title) {
      return res.status(400).json({ success: false, error: 'Title is required' });
    }

    // Mock response for now, will be replaced with actual data later
    res.status(201).json({
      success: true,
      data: { id: 3, title, description, completed: false, createdAt: new Date() }
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

/**
 * @route   PUT /api/tasks/:id
 * @desc    Update a task
 * @access  Public
 */
router.put('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const { title, description, completed } = req.body;

    // Validate request
    if (!title) {
      return res.status(400).json({ success: false, error: 'Title is required' });
    }

    // Mock response for now, will be replaced with actual data later
    res.json({
      success: true,
      data: { id: parseInt(id), title, description, completed, updatedAt: new Date() }
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

/**
 * @route   DELETE /api/tasks/:id
 * @desc    Delete a task
 * @access  Public
 */
router.delete('/:id', async (req, res) => {
  try {
    const { id } = req.params;

    // Mock response for now, will be replaced with actual data later
    res.json({
      success: true,
      message: `Task ${id} deleted successfully`
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

module.exports = router;