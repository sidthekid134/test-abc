/**
 * Test Setup
 * Configure environment and database for tests
 */

const mongoose = require('mongoose');
const { MongoMemoryServer } = require('mongodb-memory-server');

// Use in-memory MongoDB server for testing
let mongoServer;

// Connect to the in-memory database before all tests
module.exports.setupTestDB = async () => {
  try {
    mongoServer = await MongoMemoryServer.create();
    const mongoUri = mongoServer.getUri();

    await mongoose.connect(mongoUri, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });
  } catch (error) {
    console.error('Error connecting to test database:', error);
    process.exit(1);
  }
};

// Clean up database after tests
module.exports.teardownTestDB = async () => {
  try {
    await mongoose.disconnect();
    if (mongoServer) {
      await mongoServer.stop();
    }
  } catch (error) {
    console.error('Error tearing down test database:', error);
  }
};

// Clear collections between tests
module.exports.clearDatabase = async () => {
  if (mongoose.connection.readyState === 1) {
    const collections = mongoose.connection.collections;

    for (const key in collections) {
      const collection = collections[key];
      await collection.deleteMany({});
    }
  }
};

// Seed data for tests
module.exports.seedTasks = async (TaskModel) => {
  const tasks = [
    {
      title: 'Complete project proposal',
      description: 'Draft and submit project proposal by Friday',
      status: 'pending',
      priority: 'high',
      tags: ['work', 'project']
    },
    {
      title: 'Buy groceries',
      description: 'Get milk, eggs, and bread',
      status: 'completed',
      priority: 'medium',
      tags: ['personal', 'shopping']
    },
    {
      title: 'Finish coding tutorial',
      description: 'Complete React hooks tutorial',
      status: 'in_progress',
      priority: 'medium',
      tags: ['learning', 'coding']
    }
  ];

  return await TaskModel.insertMany(tasks);
};