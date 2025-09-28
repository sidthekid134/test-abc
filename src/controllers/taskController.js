/**
 * Task Controller
 * Handles business logic for task-related operations
 */

const Task = require('../models/taskModel');

/**
 * Get all tasks with filtering, pagination, and sorting
 */
exports.getTasks = async (req, res, next) => {
  try {
    // Build query
    const queryParams = { ...req.query };
    const excludeFields = ['page', 'sort', 'limit', 'fields'];
    excludeFields.forEach(field => delete queryParams[field]);

    // Filter tasks
    let query = Task.find(queryParams);

    // Sort tasks
    if (req.query.sort) {
      const sortBy = req.query.sort.split(',').join(' ');
      query = query.sort(sortBy);
    } else {
      query = query.sort('-createdAt');
    }

    // Field limiting
    if (req.query.fields) {
      const fields = req.query.fields.split(',').join(' ');
      query = query.select(fields);
    }

    // Pagination
    const page = parseInt(req.query.page, 10) || 1;
    const limit = parseInt(req.query.limit, 10) || 10;
    const skip = (page - 1) * limit;
    query = query.skip(skip).limit(limit);

    // Execute query
    const tasks = await query;
    const count = await Task.countDocuments(queryParams);

    // Return response
    res.status(200).json({
      success: true,
      count,
      pagination: {
        page,
        limit,
        totalPages: Math.ceil(count / limit)
      },
      data: tasks
    });
  } catch (error) {
    next(error);
  }
};

/**
 * Get single task by ID
 */
exports.getTaskById = async (req, res, next) => {
  try {
    const task = await Task.findById(req.params.id);

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
    // Handle invalid ObjectId format
    if (error.name === 'CastError') {
      return res.status(400).json({
        success: false,
        error: 'Invalid task ID format'
      });
    }
    next(error);
  }
};

/**
 * Create new task
 */
exports.createTask = async (req, res, next) => {
  try {
    // Additional validation can be added here
    const validation = Task.validateTask(req.body);
    if (!validation.isValid) {
      return res.status(400).json({
        success: false,
        errors: validation.errors
      });
    }

    const task = await Task.create(req.body);

    res.status(201).json({
      success: true,
      data: task
    });
  } catch (error) {
    // Mongoose validation error
    if (error.name === 'ValidationError') {
      const errors = Object.values(error.errors).map(err => err.message);
      return res.status(400).json({
        success: false,
        errors
      });
    }
    next(error);
  }
};

/**
 * Update task by ID
 */
exports.updateTask = async (req, res, next) => {
  try {
    // Additional validation
    const validation = Task.validateTask(req.body);
    if (!validation.isValid) {
      return res.status(400).json({
        success: false,
        errors: validation.errors
      });
    }

    const task = await Task.findByIdAndUpdate(
      req.params.id,
      req.body,
      {
        new: true,
        runValidators: true
      }
    );

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
    // Handle different types of errors
    if (error.name === 'CastError') {
      return res.status(400).json({
        success: false,
        error: 'Invalid task ID format'
      });
    }
    if (error.name === 'ValidationError') {
      const errors = Object.values(error.errors).map(err => err.message);
      return res.status(400).json({
        success: false,
        errors
      });
    }
    next(error);
  }
};

/**
 * Delete task by ID
 */
exports.deleteTask = async (req, res, next) => {
  try {
    const task = await Task.findByIdAndDelete(req.params.id);

    if (!task) {
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
    // Handle invalid ObjectId format
    if (error.name === 'CastError') {
      return res.status(400).json({
        success: false,
        error: 'Invalid task ID format'
      });
    }
    next(error);
  }
};