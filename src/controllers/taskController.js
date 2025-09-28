/**
 * Task Controller
 *
 * Contains all the business logic for task operations
 */
const Task = require('../models/task');

/**
 * Get all tasks
 * @route GET /api/tasks
 */
const getAllTasks = async (req, res) => {
  try {
    const tasks = await Task.find({});

    res.json({
      success: true,
      count: tasks.length,
      data: tasks
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
};

/**
 * Get task by ID
 * @route GET /api/tasks/:id
 */
const getTaskById = async (req, res) => {
  try {
    const task = await Task.findById(req.params.id);

    if (!task) {
      return res.status(404).json({
        success: false,
        error: 'Task not found'
      });
    }

    res.json({
      success: true,
      data: task
    });
  } catch (error) {
    // Handle invalid ObjectId format
    if (error.kind === 'ObjectId') {
      return res.status(404).json({
        success: false,
        error: 'Task not found'
      });
    }

    res.status(500).json({
      success: false,
      error: error.message
    });
  }
};

/**
 * Create a new task
 * @route POST /api/tasks
 */
const createTask = async (req, res) => {
  try {
    const newTask = new Task(req.body);
    await newTask.save();

    res.status(201).json({
      success: true,
      data: newTask
    });
  } catch (error) {
    // Validation error
    if (error.name === 'ValidationError') {
      const messages = Object.values(error.errors).map(val => val.message);

      return res.status(400).json({
        success: false,
        error: messages.join(', ')
      });
    }

    res.status(500).json({
      success: false,
      error: error.message
    });
  }
};

/**
 * Update a task
 * @route PUT /api/tasks/:id
 */
const updateTask = async (req, res) => {
  try {
    // Validate the update fields
    Task.validateUpdate(req.body);

    const task = await Task.findById(req.params.id);

    if (!task) {
      return res.status(404).json({
        success: false,
        error: 'Task not found'
      });
    }

    // Update the task
    const updatedTask = await Task.findByIdAndUpdate(
      req.params.id,
      req.body,
      {
        new: true,
        runValidators: true
      }
    );

    res.json({
      success: true,
      data: updatedTask
    });
  } catch (error) {
    // Handle validation errors
    if (error.name === 'ValidationError') {
      const messages = Object.values(error.errors).map(val => val.message);

      return res.status(400).json({
        success: false,
        error: messages.join(', ')
      });
    }

    // Handle invalid ObjectId format
    if (error.kind === 'ObjectId') {
      return res.status(404).json({
        success: false,
        error: 'Task not found'
      });
    }

    res.status(500).json({
      success: false,
      error: error.message
    });
  }
};

/**
 * Delete a task
 * @route DELETE /api/tasks/:id
 */
const deleteTask = async (req, res) => {
  try {
    const task = await Task.findById(req.params.id);

    if (!task) {
      return res.status(404).json({
        success: false,
        error: 'Task not found'
      });
    }

    await Task.findByIdAndDelete(req.params.id);

    res.json({
      success: true,
      data: {},
      message: 'Task deleted successfully'
    });
  } catch (error) {
    // Handle invalid ObjectId format
    if (error.kind === 'ObjectId') {
      return res.status(404).json({
        success: false,
        error: 'Task not found'
      });
    }

    res.status(500).json({
      success: false,
      error: error.message
    });
  }
};

module.exports = {
  getAllTasks,
  getTaskById,
  createTask,
  updateTask,
  deleteTask
};