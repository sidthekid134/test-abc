const Task = require('../models/Task');

/**
 * Task controller for handling task-related operations
 */
const taskController = {
  /**
   * Get all tasks with filtering and pagination
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   * @param {Function} next - Express next middleware function
   */
  getAllTasks: async (req, res, next) => {
    try {
      // Build query
      const queryObj = { ...req.query };

      // Exclude special fields
      const excludedFields = ['page', 'sort', 'limit', 'fields'];
      excludedFields.forEach(field => delete queryObj[field]);

      // Advanced filtering
      let queryStr = JSON.stringify(queryObj);
      queryStr = queryStr.replace(/\b(gte|gt|lte|lt)\b/g, match => `$${match}`);

      let query = Task.find(JSON.parse(queryStr));

      // Sorting
      if (req.query.sort) {
        const sortBy = req.query.sort.split(',').join(' ');
        query = query.sort(sortBy);
      } else {
        query = query.sort('-createdAt');
      }

      // Pagination
      const page = parseInt(req.query.page, 10) || 1;
      const limit = parseInt(req.query.limit, 10) || 100;
      const skip = (page - 1) * limit;

      query = query.skip(skip).limit(limit);

      // Execute query
      const tasks = await query;

      // Count total documents for pagination info
      const totalTasks = await Task.countDocuments(JSON.parse(queryStr));

      res.status(200).json({
        status: 'success',
        results: tasks.length,
        total: totalTasks,
        pagination: {
          currentPage: page,
          totalPages: Math.ceil(totalTasks / limit),
          limit
        },
        data: {
          tasks
        }
      });
    } catch (error) {
      next(error);
    }
  },

  /**
   * Get a specific task by ID
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   * @param {Function} next - Express next middleware function
   */
  getTaskById: async (req, res, next) => {
    try {
      const task = await Task.findById(req.params.id);

      if (!task) {
        const error = new Error('Task not found');
        error.statusCode = 404;
        throw error;
      }

      res.status(200).json({
        status: 'success',
        data: {
          task
        }
      });
    } catch (error) {
      // Handle invalid ID format
      if (error.name === 'CastError') {
        const castError = new Error('Invalid task ID format');
        castError.statusCode = 400;
        return next(castError);
      }
      next(error);
    }
  },

  /**
   * Create a new task
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   * @param {Function} next - Express next middleware function
   */
  createTask: async (req, res, next) => {
    try {
      // Schema validation will handle required fields
      const newTask = await Task.create(req.body);

      res.status(201).json({
        status: 'success',
        data: {
          task: newTask
        }
      });
    } catch (error) {
      // Mongoose validation error
      if (error.name === 'ValidationError') {
        const messages = Object.values(error.errors).map(val => val.message);
        const validationError = new Error(messages.join('. '));
        validationError.statusCode = 400;
        return next(validationError);
      }
      next(error);
    }
  },

  /**
   * Update an existing task
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   * @param {Function} next - Express next middleware function
   */
  updateTask: async (req, res, next) => {
    try {
      const task = await Task.findByIdAndUpdate(
        req.params.id,
        req.body,
        {
          new: true, // Return updated document
          runValidators: true // Run validators on update
        }
      );

      if (!task) {
        const error = new Error('Task not found');
        error.statusCode = 404;
        throw error;
      }

      res.status(200).json({
        status: 'success',
        data: {
          task
        }
      });
    } catch (error) {
      // Handle invalid ID format
      if (error.name === 'CastError') {
        const castError = new Error('Invalid task ID format');
        castError.statusCode = 400;
        return next(castError);
      }
      // Mongoose validation error
      if (error.name === 'ValidationError') {
        const messages = Object.values(error.errors).map(val => val.message);
        const validationError = new Error(messages.join('. '));
        validationError.statusCode = 400;
        return next(validationError);
      }
      next(error);
    }
  },

  /**
   * Delete a task
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   * @param {Function} next - Express next middleware function
   */
  deleteTask: async (req, res, next) => {
    try {
      const task = await Task.findByIdAndDelete(req.params.id);

      if (!task) {
        const error = new Error('Task not found');
        error.statusCode = 404;
        throw error;
      }

      res.status(204).send();
    } catch (error) {
      // Handle invalid ID format
      if (error.name === 'CastError') {
        const castError = new Error('Invalid task ID format');
        castError.statusCode = 400;
        return next(castError);
      }
      next(error);
    }
  }
};

module.exports = taskController;