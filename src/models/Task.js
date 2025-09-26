/**
 * Task model (in-memory implementation for MVP)
 */

// In-memory array to store tasks
let tasks = [];
let nextId = 1;

class Task {
  /**
   * Get all tasks
   * @returns {Array} Array of tasks
   */
  static getAll() {
    return tasks;
  }

  /**
   * Get task by ID
   * @param {number} id - Task ID
   * @returns {Object|null} Task object or null if not found
   */
  static getById(id) {
    return tasks.find(task => task.id === parseInt(id)) || null;
  }

  /**
   * Create a new task
   * @param {Object} taskData - Task data
   * @returns {Object} Created task
   */
  static create(taskData) {
    const task = {
      id: nextId++,
      title: taskData.title,
      description: taskData.description || '',
      status: taskData.status || 'pending',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };

    tasks.push(task);
    return task;
  }

  /**
   * Update an existing task
   * @param {number} id - Task ID
   * @param {Object} taskData - Updated task data
   * @returns {Object|null} Updated task or null if not found
   */
  static update(id, taskData) {
    const index = tasks.findIndex(task => task.id === parseInt(id));

    if (index === -1) return null;

    const updatedTask = {
      ...tasks[index],
      ...taskData,
      updatedAt: new Date().toISOString()
    };

    tasks[index] = updatedTask;
    return updatedTask;
  }

  /**
   * Delete a task
   * @param {number} id - Task ID
   * @returns {boolean} True if deleted, false if not found
   */
  static delete(id) {
    const index = tasks.findIndex(task => task.id === parseInt(id));

    if (index === -1) return false;

    tasks.splice(index, 1);
    return true;
  }
}

module.exports = Task;