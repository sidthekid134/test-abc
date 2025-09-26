/**
 * Test setup configuration
 */
const mongoose = require('mongoose');
const { MongoMemoryServer } = require('mongodb-memory-server');

let mongoServer;

/**
 * Connect to the in-memory database before tests run
 */
beforeAll(async () => {
  // Create an in-memory MongoDB server
  mongoServer = await MongoMemoryServer.create();
  const uri = mongoServer.getUri();

  // Set environment variables for testing
  process.env.NODE_ENV = 'test';
  process.env.MONGODB_URI_TEST = uri;

  // Connect to the in-memory database
  await mongoose.connect(uri);
});

/**
 * Clear database collections between tests
 */
afterEach(async () => {
  const collections = mongoose.connection.collections;

  for (const key in collections) {
    const collection = collections[key];
    await collection.deleteMany({});
  }
});

/**
 * Disconnect from in-memory database and close server after tests
 */
afterAll(async () => {
  await mongoose.disconnect();
  await mongoServer.stop();
});