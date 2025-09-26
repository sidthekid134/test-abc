const Task = require('../models/Task');

/**
 * Task controller for handling task-related operations
 */
const taskController = {
  /**
   * Get all tasks
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   * @param {Function} next - Express next middleware function
   */
  getAllTasks: (req, res, next) => {
    try {
      const tasks = Task.getAll();
      res.status(200).json({
        status: 'success',
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
  getTaskById: (req, res, next) => {
    try {
      const { id } = req.params;
      const task = Task.getById(id);

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
      next(error);
    }
  },

  /**
   * Create a new task
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   * @param {Function} next - Express next middleware function
   */
  createTask: (req, res, next) => {
    try {
      // Simple validation
      if (!req.body.title) {
        const error = new Error('Title is required');
        error.statusCode = 400;
        throw error;
      }

      const newTask = Task.create(req.body);

      res.status(201).json({
        status: 'success',
        data: {
          task: newTask
        }
      });
    } catch (error) {
      next(error);
    }
  },

  /**
   * Update an existing task
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   * @param {Function} next - Express next middleware function
   */
  updateTask: (req, res, next) => {
    try {
      const { id } = req.params;
      const updatedTask = Task.update(id, req.body);

      if (!updatedTask) {
        const error = new Error('Task not found');
        error.statusCode = 404;
        throw error;
      }

      res.status(200).json({
        status: 'success',
        data: {
          task: updatedTask
        }
      });
    } catch (error) {
      next(error);
    }
  },

  /**
   * Delete a task
   * @param {Object} req - Express request object
   * @param {Object} res - Express response object
   * @param {Function} next - Express next middleware function
   */
  deleteTask: (req, res, next) => {
    try {
      const { id } = req.params;
      const deleted = Task.delete(id);

      if (!deleted) {
        const error = new Error('Task not found');
        error.statusCode = 404;
        throw error;
      }

      res.status(204).send();
    } catch (error) {
      next(error);
    }
  }
};

module.exports = taskController;