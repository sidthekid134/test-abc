import React, { useState, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import TaskList from '../components/TaskList';
import TaskForm from '../components/TaskForm';
import TaskFilter from '../components/TaskFilter';
import { Task, TaskFormData, TaskFilter as FilterType, SortOption, SortDirection } from '../types/Task';
import { getStoredTasks, storeTasks, addTask, updateTask, deleteTask } from '../services/localStorage';

const TasksPage: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isAddingTask, setIsAddingTask] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  
  // Filtering and sorting state
  const [filter, setFilter] = useState<FilterType>({
    status: 'all',
    priority: 'all',
    searchTerm: ''
  });
  const [sortOption, setSortOption] = useState<SortOption>('createdAt');
  const [sortDirection, setSortDirection] = useState<SortDirection>('desc');

  // Load tasks from local storage
  useEffect(() => {
    const loadTasks = () => {
      try {
        setIsLoading(true);
        const storedTasks = getStoredTasks();
        setTasks(storedTasks);
        setError(null);
      } catch (err) {
        console.error('Failed to load tasks:', err);
        setError('Failed to load tasks. Please refresh the page.');
      } finally {
        setIsLoading(false);
      }
    };

    loadTasks();
  }, []);

  // Handle creating a new task
  const handleAddTask = (taskData: TaskFormData) => {
    try {
      const newTask: Task = {
        id: uuidv4(),
        ...taskData,
        createdAt: new Date(),
        updatedAt: new Date()
      };
      
      addTask(newTask);
      setTasks(prevTasks => [newTask, ...prevTasks]);
      setIsAddingTask(false);
    } catch (err) {
      console.error('Failed to add task:', err);
      throw new Error('Failed to add task. Please try again.');
    }
  };

  // Handle updating an existing task
  const handleUpdateTask = (taskData: TaskFormData) => {
    if (!editingTask) return;

    try {
      const updatedTask: Task = {
        ...editingTask,
        ...taskData,
        updatedAt: new Date()
      };
      
      const success = updateTask(updatedTask);
      
      if (success) {
        setTasks(prevTasks => 
          prevTasks.map(task => 
            task.id === updatedTask.id ? updatedTask : task
          )
        );
        setEditingTask(null);
      } else {
        throw new Error('Task not found.');
      }
    } catch (err) {
      console.error('Failed to update task:', err);
      throw new Error('Failed to update task. Please try again.');
    }
  };

  // Handle deleting a task
  const handleDeleteTask = (taskId: string) => {
    try {
      const success = deleteTask(taskId);
      
      if (success) {
        setTasks(prevTasks => prevTasks.filter(task => task.id !== taskId));
      } else {
        console.warn('Task not found for deletion:', taskId);
      }
    } catch (err) {
      console.error('Failed to delete task:', err);
      setError('Failed to delete task. Please try again.');
    }
  };

  // Handle toggling task completion
  const handleToggleComplete = (task: Task) => {
    const updatedTask: Task = {
      ...task,
      completed: !task.completed,
      updatedAt: new Date()
    };
    
    try {
      const success = updateTask(updatedTask);
      
      if (success) {
        setTasks(prevTasks => 
          prevTasks.map(t => 
            t.id === updatedTask.id ? updatedTask : t
          )
        );
      }
    } catch (err) {
      console.error('Failed to toggle task completion:', err);
      setError('Failed to update task. Please try again.');
    }
  };

  return (
    <div>
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900">My Tasks</h1>
        <button
          onClick={() => setIsAddingTask(true)}
          className="mt-3 sm:mt-0 flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          Add Task
        </button>
      </div>

      {error && (
        <div className="mb-4 p-4 bg-red-50 border-l-4 border-red-400 text-red-700" role="alert">
          <p>{error}</p>
        </div>
      )}

      {(isAddingTask || editingTask) && (
        <div className="mb-6">
          <TaskForm 
            initialTask={editingTask || undefined}
            onSubmit={editingTask ? handleUpdateTask : handleAddTask}
            onCancel={() => {
              setIsAddingTask(false);
              setEditingTask(null);
            }}
          />
        </div>
      )}
      
      <TaskFilter
        filter={filter}
        sortOption={sortOption}
        sortDirection={sortDirection}
        onFilterChange={setFilter}
        onSortChange={setSortOption}
        onSortDirectionChange={setSortDirection}
      />

      <TaskList 
        tasks={tasks}
        filter={filter}
        sortOption={sortOption}
        sortDirection={sortDirection}
        onEditTask={setEditingTask}
        onDeleteTask={handleDeleteTask}
        onToggleComplete={handleToggleComplete}
        isLoading={isLoading}
      />
    </div>
  );
};

export default TasksPage;