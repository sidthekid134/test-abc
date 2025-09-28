/**
 * Jest Configuration
 * Configure test environment and settings
 */

module.exports = {
  // Test environment
  testEnvironment: 'node',

  // Test file patterns
  testMatch: [
    '**/tests/**/*.test.js',
    '**/__tests__/**/*.js'
  ],

  // Test coverage collection
  collectCoverage: true,
  collectCoverageFrom: [
    'src/**/*.js',
    '!src/tests/**/*.js',
    '!**/node_modules/**'
  ],

  // Coverage reporting
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov'],

  // Test timeout
  testTimeout: 10000,

  // Verbose output
  verbose: true
};