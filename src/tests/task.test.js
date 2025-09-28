/**
 * Task API Tests
 * Tests for task management endpoints
 */

const request = require('supertest');
const mongoose = require('mongoose');
const app = require('../../server');
const Task = require('../models/taskModel');
const { setupTestDB, teardownTestDB, clearDatabase, seedTasks } = require('./setup');
const config = require('../config/config');

const API_BASE_URL = `${config.api.prefix}/${config.api.version}/tasks`;

// Setup and teardown for all tests
beforeAll(async () => {
  await setupTestDB();
});

afterAll(async () => {
  await teardownTestDB();
});

// Clear database and seed tasks before each test
beforeEach(async () => {
  await clearDatabase();
  await seedTasks(Task);
});

describe('Task API Endpoints', () => {
  // GET all tasks
  describe('GET /tasks', () => {
    it('should return all tasks', async () => {
      const res = await request(app).get(API_BASE_URL);

      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);
      expect(Array.isArray(res.body.data)).toBe(true);
      expect(res.body.data.length).toBe(3);
    });

    it('should filter tasks by status', async () => {
      const res = await request(app).get(`${API_BASE_URL}?status=completed`);

      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);
      expect(res.body.data.length).toBe(1);
      expect(res.body.data[0].status).toBe('completed');
    });

    it('should sort tasks by priority', async () => {
      const res = await request(app).get(`${API_BASE_URL}?sort=priority`);

      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);
      expect(Array.isArray(res.body.data)).toBe(true);
    });

    it('should paginate results', async () => {
      const res = await request(app).get(`${API_BASE_URL}?page=1&limit=2`);

      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);
      expect(res.body.data.length).toBe(2);
      expect(res.body.pagination).toBeDefined();
      expect(res.body.pagination.page).toBe(1);
      expect(res.body.pagination.limit).toBe(2);
    });
  });

  // GET single task
  describe('GET /tasks/:id', () => {
    it('should get a single task by ID', async () => {
      const tasks = await Task.find();
      const taskId = tasks[0]._id;

      const res = await request(app).get(`${API_BASE_URL}/${taskId}`);

      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);
      expect(res.body.data._id.toString()).toBe(taskId.toString());
    });

    it('should return 404 for non-existent task ID', async () => {
      const nonExistentId = new mongoose.Types.ObjectId();

      const res = await request(app).get(`${API_BASE_URL}/${nonExistentId}`);

      expect(res.status).toBe(404);
      expect(res.body.success).toBe(false);
    });

    it('should return 400 for invalid task ID format', async () => {
      const res = await request(app).get(`${API_BASE_URL}/invalidid123`);

      expect(res.status).toBe(400);
      expect(res.body.success).toBe(false);
    });
  });

  // CREATE task
  describe('POST /tasks', () => {
    it('should create a new task with valid data', async () => {
      const newTask = {
        title: 'New test task',
        description: 'This is a test task created by automated tests',
        status: 'pending',
        priority: 'high',
        tags: ['test', 'automation']
      };

      const res = await request(app)
        .post(API_BASE_URL)
        .send(newTask);

      expect(res.status).toBe(201);
      expect(res.body.success).toBe(true);
      expect(res.body.data.title).toBe(newTask.title);
      expect(res.body.data.description).toBe(newTask.description);
      expect(res.body.data.status).toBe(newTask.status);
      expect(res.body.data.priority).toBe(newTask.priority);
    });

    it('should return 400 when title is missing', async () => {
      const invalidTask = {
        description: 'Missing title',
        status: 'pending'
      };

      const res = await request(app)
        .post(API_BASE_URL)
        .send(invalidTask);

      expect(res.status).toBe(400);
      expect(res.body.success).toBe(false);
      expect(res.body.errors).toBeDefined();
    });

    it('should return 400 for invalid status value', async () => {
      const invalidTask = {
        title: 'Invalid status task',
        status: 'invalid_status'
      };

      const res = await request(app)
        .post(API_BASE_URL)
        .send(invalidTask);

      expect(res.status).toBe(400);
      expect(res.body.success).toBe(false);
    });
  });

  // UPDATE task
  describe('PUT /tasks/:id', () => {
    it('should update a task with valid data', async () => {
      const tasks = await Task.find();
      const taskId = tasks[0]._id;

      const updateData = {
        title: 'Updated task title',
        status: 'completed'
      };

      const res = await request(app)
        .put(`${API_BASE_URL}/${taskId}`)
        .send(updateData);

      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);
      expect(res.body.data.title).toBe(updateData.title);
      expect(res.body.data.status).toBe(updateData.status);
    });

    it('should return 404 for non-existent task ID', async () => {
      const nonExistentId = new mongoose.Types.ObjectId();

      const res = await request(app)
        .put(`${API_BASE_URL}/${nonExistentId}`)
        .send({ title: 'Updated title' });

      expect(res.status).toBe(404);
      expect(res.body.success).toBe(false);
    });

    it('should return 400 for invalid update data', async () => {
      const tasks = await Task.find();
      const taskId = tasks[0]._id;

      const invalidData = {
        status: 'invalid_status'
      };

      const res = await request(app)
        .put(`${API_BASE_URL}/${taskId}`)
        .send(invalidData);

      expect(res.status).toBe(400);
      expect(res.body.success).toBe(false);
    });
  });

  // DELETE task
  describe('DELETE /tasks/:id', () => {
    it('should delete a task by ID', async () => {
      const tasks = await Task.find();
      const taskId = tasks[0]._id;

      const res = await request(app).delete(`${API_BASE_URL}/${taskId}`);

      expect(res.status).toBe(200);
      expect(res.body.success).toBe(true);

      // Verify task is deleted
      const deletedTask = await Task.findById(taskId);
      expect(deletedTask).toBeNull();
    });

    it('should return 404 for non-existent task ID', async () => {
      const nonExistentId = new mongoose.Types.ObjectId();

      const res = await request(app).delete(`${API_BASE_URL}/${nonExistentId}`);

      expect(res.status).toBe(404);
      expect(res.body.success).toBe(false);
    });

    it('should return 400 for invalid task ID format', async () => {
      const res = await request(app).delete(`${API_BASE_URL}/invalidid123`);

      expect(res.status).toBe(400);
      expect(res.body.success).toBe(false);
    });
  });
});