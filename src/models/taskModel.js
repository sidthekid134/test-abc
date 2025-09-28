/**
 * Task Model
 * Mongoose schema for tasks with validation and methods.
 */
const mongoose = require('mongoose');
const Schema = mongoose.Schema;

// Task schema definition
const TaskSchema = new Schema({
  title: {
    type: String,
    required: [true, 'Title is required'],
    trim: true,
    maxlength: [100, 'Title cannot be more than 100 characters']
  },
  description: {
    type: String,
    trim: true,
    default: ''
  },
  status: {
    type: String,
    enum: {
      values: ['pending', 'in_progress', 'completed'],
      message: '{VALUE} is not a valid status'
    },
    default: 'pending'
  },
  dueDate: {
    type: Date,
    default: null
  },
  priority: {
    type: String,
    enum: {
      values: ['low', 'medium', 'high'],
      message: '{VALUE} is not a valid priority'
    },
    default: 'medium'
  },
  tags: [{
    type: String,
    trim: true
  }]
}, { timestamps: true });

// Create index for faster searches
TaskSchema.index({ status: 1 });
TaskSchema.index({ priority: 1 });

// Static method to validate task data
TaskSchema.statics.validateTask = function(data) {
  const errors = [];

  // Basic validation checks
  if (data.status && !['pending', 'in_progress', 'completed'].includes(data.status)) {
    errors.push('Status must be one of: pending, in_progress, completed');
  }

  if (data.priority && !['low', 'medium', 'high'].includes(data.priority)) {
    errors.push('Priority must be one of: low, medium, high');
  }

  if (data.dueDate && isNaN(new Date(data.dueDate).getTime())) {
    errors.push('Due date must be a valid date');
  }

  if (data.tags && !Array.isArray(data.tags)) {
    errors.push('Tags must be an array');
  }

  return {
    isValid: errors.length === 0,
    errors
  };
};

// Pre-save hook to update timestamps
TaskSchema.pre('save', function(next) {
  this.updatedAt = new Date();
  next();
});

module.exports = mongoose.model('Task', TaskSchema);