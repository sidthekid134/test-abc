/**
 * Task model (MongoDB implementation)
 */
const mongoose = require('mongoose');

/**
 * Task schema definition
 */
const taskSchema = new mongoose.Schema(
  {
    title: {
      type: String,
      required: [true, 'A task must have a title'],
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
        values: ['pending', 'in-progress', 'completed'],
        message: 'Status must be: pending, in-progress, or completed'
      },
      default: 'pending'
    },
    priority: {
      type: String,
      enum: {
        values: ['low', 'medium', 'high'],
        message: 'Priority must be: low, medium, or high'
      },
      default: 'medium'
    },
    dueDate: {
      type: Date,
      default: null
    }
  },
  {
    timestamps: true,
    toJSON: { virtuals: true },
    toObject: { virtuals: true }
  }
);

// Add any indexes for improved query performance
taskSchema.index({ status: 1 });
taskSchema.index({ priority: 1 });

/**
 * Pre-save middleware
 */
taskSchema.pre('save', function(next) {
  // Any pre-save operations can go here
  next();
});

/**
 * Instance methods
 */
taskSchema.methods.isPastDue = function() {
  if (!this.dueDate) return false;
  return new Date() > this.dueDate;
};

/**
 * Static methods
 */
taskSchema.statics.findByStatus = function(status) {
  return this.find({ status });
};

// Create and export model
const Task = mongoose.model('Task', taskSchema);
module.exports = Task;