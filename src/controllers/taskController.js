const Task = require('../models/Task');
const asyncHandler = require('../middleware/asyncHandler');

// @desc    Get all tasks
// @route   GET /api/tasks
// @access  Public
exports.getAllTasks = asyncHandler(async (req, res) => {
  // Support basic filtering
  const filter = {};
  if (req.query.status) filter.status = req.query.status;
  if (req.query.priority) filter.priority = req.query.priority;
  
  // Get tasks with optional filters
  const tasks = await Task.find(filter);
  
  res.status(200).json({
    success: true,
    count: tasks.length,
    data: tasks
  });
});

// @desc    Get single task by ID
// @route   GET /api/tasks/:id
// @access  Public
exports.getTaskById = asyncHandler(async (req, res) => {
  const task = await Task.findById(req.params.id);
  
  if (!task) {
    return res.status(404).json({
      success: false,
      message: `Task not found with id of ${req.params.id}`
    });
  }
  
  res.status(200).json({
    success: true,
    data: task
  });
});

// @desc    Create a new task
// @route   POST /api/tasks
// @access  Public
exports.createTask = asyncHandler(async (req, res) => {
  // Create task
  const task = await Task.create(req.body);
  
  res.status(201).json({
    success: true,
    data: task
  });
});

// @desc    Update a task
// @route   PUT /api/tasks/:id
// @access  Public
exports.updateTask = asyncHandler(async (req, res) => {
  // Find and update task
  const task = await Task.findByIdAndUpdate(req.params.id, req.body, {
    new: true,
    runValidators: true
  });
  
  if (!task) {
    return res.status(404).json({
      success: false,
      message: `Task not found with id of ${req.params.id}`
    });
  }
  
  res.status(200).json({
    success: true,
    data: task
  });
});

// @desc    Delete a task
// @route   DELETE /api/tasks/:id
// @access  Public
exports.deleteTask = asyncHandler(async (req, res) => {
  const task = await Task.findById(req.params.id);
  
  if (!task) {
    return res.status(404).json({
      success: false,
      message: `Task not found with id of ${req.params.id}`
    });
  }
  
  await task.deleteOne();
  
  res.status(200).json({
    success: true,
    data: {}
  });
});