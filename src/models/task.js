/**
 * Task Model
 *
 * This is a simple mock model for tasks. In a real application, this would
 * interact with a database using an ORM like Sequelize or Mongoose.
 */

class Task {
  constructor(id, title, description = '', completed = false) {
    this.id = id;
    this.title = title;
    this.description = description;
    this.completed = completed;
    this.createdAt = new Date();
    this.updatedAt = new Date();
  }

  // Static methods to be replaced with actual database operations in the future
  static getAll() {
    return [
      new Task(1, 'Task 1', 'Description for Task 1'),
      new Task(2, 'Task 2', 'Description for Task 2', true)
    ];
  }

  static getById(id) {
    const parsedId = parseInt(id);
    const tasks = this.getAll();
    return tasks.find(task => task.id === parsedId) || null;
  }

  static create(taskData) {
    const { title, description } = taskData;
    const tasks = this.getAll();
    const id = tasks.length + 1;
    const newTask = new Task(id, title, description);
    return newTask;
  }

  static update(id, taskData) {
    const parsedId = parseInt(id);
    const { title, description, completed } = taskData;
    const task = this.getById(parsedId);

    if (!task) return null;

    task.title = title || task.title;
    task.description = description || task.description;
    task.completed = completed !== undefined ? completed : task.completed;
    task.updatedAt = new Date();

    return task;
  }

  static delete(id) {
    const parsedId = parseInt(id);
    const tasks = this.getAll();
    const index = tasks.findIndex(task => task.id === parsedId);

    if (index === -1) return false;

    return true;
  }
}

module.exports = Task;