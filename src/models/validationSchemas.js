/**
 * Validation schemas for request validation
 */

// Task validation schema
const taskSchema = {
  title: {
    required: true,
    type: 'string',
    minLength: 3,
    maxLength: 100
  },
  description: {
    required: false,
    type: 'string',
    maxLength: 500
  },
  status: {
    required: false,
    type: 'string',
    enum: ['todo', 'in-progress', 'completed']
  },
  priority: {
    required: false,
    type: 'string',
    enum: ['low', 'medium', 'high']
  },
  dueDate: {
    required: false,
    type: 'date'
  },
  createdBy: {
    required: true,
    type: 'string'
  },
  completed: {
    required: false,
    type: 'boolean'
  }
};

module.exports = {
  taskSchema
};