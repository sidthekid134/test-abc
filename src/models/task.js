/**
 * Task Model
 *
 * Mongoose schema for tasks with validation
 */
const mongoose = require('mongoose');

const TaskSchema = new mongoose.Schema(
  {
    title: {
      type: String,
      required: [true, 'Task title is required'],
      trim: true,
      maxlength: [100, 'Task title cannot be more than 100 characters']
    },
    description: {
      type: String,
      trim: true,
      default: '',
      maxlength: [500, 'Task description cannot be more than 500 characters']
    },
    completed: {
      type: Boolean,
      default: false
    },
    priority: {
      type: String,
      enum: ['low', 'medium', 'high'],
      default: 'medium'
    },
    dueDate: {
      type: Date,
      default: null
    }
  },
  {
    timestamps: true
  }
);

// Add index for better performance on common queries
TaskSchema.index({ completed: 1 });

/**
 * Custom validation middleware for task updates
 * Ensures at least one field is provided when updating
 */
TaskSchema.statics.validateUpdate = function (updateData) {
  const updates = Object.keys(updateData);
  const allowedUpdates = ['title', 'description', 'completed', 'priority', 'dueDate'];
  const isValidOperation = updates.some(update => allowedUpdates.includes(update));

  if (!isValidOperation) {
    throw new Error('No valid update fields provided');
  }

  return true;
};

module.exports = mongoose.model('Task', TaskSchema);