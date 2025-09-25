const express = require('express');
const router = express.Router();
const taskController = require('../controllers/taskController');
const validateRequest = require('../middleware/validateRequest');
const { taskSchema } = require('../models/validationSchemas');

// GET all tasks
router.get('/', taskController.getAllTasks);

// GET a single task by ID
router.get('/:id', taskController.getTaskById);

// POST a new task
router.post('/', validateRequest(taskSchema), taskController.createTask);

// PUT/update a task
router.put('/:id', validateRequest(taskSchema), taskController.updateTask);

// DELETE a task
router.delete('/:id', taskController.deleteTask);

module.exports = router;