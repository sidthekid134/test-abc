import React from 'react';

const AboutPage: React.FC = () => {
  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-6">About Task Management MVP</h1>
      
      <div className="bg-white shadow rounded-lg p-6 mb-6">
        <h2 className="text-xl font-semibold mb-3">Overview</h2>
        <p className="text-gray-700 mb-4">
          This simple but powerful task management application allows you to organize and track your tasks efficiently. 
          Built with modern web technologies, it provides a smooth and responsive user experience.
        </p>
        <p className="text-gray-700">
          This is an MVP (Minimum Viable Product) version focused on core functionality.
        </p>
      </div>
      
      <div className="bg-white shadow rounded-lg p-6 mb-6">
        <h2 className="text-xl font-semibold mb-3">Key Features</h2>
        <ul className="list-disc pl-5 text-gray-700 space-y-2">
          <li>Create, read, update, and delete tasks</li>
          <li>Mark tasks as complete/incomplete</li>
          <li>Set priority levels for tasks</li>
          <li>Filter tasks by status and priority</li>
          <li>Search tasks by keywords</li>
          <li>Sort tasks by different criteria</li>
          <li>Local storage for data persistence</li>
          <li>Clean, responsive user interface</li>
        </ul>
      </div>
      
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-3">Technology Stack</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <h3 className="text-lg font-medium text-gray-900">Frontend:</h3>
            <ul className="list-disc pl-5 text-gray-700 space-y-1">
              <li>React for UI components</li>
              <li>TypeScript for type safety</li>
              <li>React Router for navigation</li>
              <li>Tailwind CSS for styling</li>
            </ul>
          </div>
          <div>
            <h3 className="text-lg font-medium text-gray-900">Storage:</h3>
            <ul className="list-disc pl-5 text-gray-700 space-y-1">
              <li>Browser Local Storage</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AboutPage;