/**
 * Task Model
 * This is a placeholder model that will be replaced with a proper database model
 * in a future implementation. It defines the structure and validation for tasks.
 */

class Task {
  constructor(data) {
    this.id = data.id || Date.now().toString();
    this.title = data.title;
    this.description = data.description || '';
    this.status = data.status || 'pending'; // pending, in_progress, completed
    this.createdAt = data.createdAt || new Date().toISOString();
    this.updatedAt = data.updatedAt || null;
  }

  // Validate task data
  static validate(data) {
    const errors = [];

    if (!data.title) {
      errors.push('Title is required');
    }

    if (data.status && !['pending', 'in_progress', 'completed'].includes(data.status)) {
      errors.push('Status must be one of: pending, in_progress, completed');
    }

    return {
      isValid: errors.length === 0,
      errors
    };
  }

  // In a real implementation, these methods would interact with a database
  static async findAll() {
    return [];
  }

  static async findById(id) {
    return null;
  }

  static async create(data) {
    const validation = this.validate(data);

    if (!validation.isValid) {
      throw new Error(validation.errors.join(', '));
    }

    return new Task(data);
  }

  static async update(id, data) {
    const validation = this.validate(data);

    if (!validation.isValid) {
      throw new Error(validation.errors.join(', '));
    }

    return new Task({ ...data, id, updatedAt: new Date().toISOString() });
  }

  static async delete(id) {
    return true;
  }
}

module.exports = Task;