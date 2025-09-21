import React from 'react';
import { Task, TaskFilter, SortOption, SortDirection } from '../types/Task';
import TaskItem from './TaskItem';

interface TaskListProps {
  tasks: Task[];
  filter: TaskFilter;
  sortOption: SortOption;
  sortDirection: SortDirection;
  onEditTask: (task: Task) => void;
  onDeleteTask: (taskId: string) => void;
  onToggleComplete: (task: Task) => void;
  isLoading: boolean;
}

const TaskList: React.FC<TaskListProps> = ({
  tasks,
  filter,
  sortOption,
  sortDirection,
  onEditTask,
  onDeleteTask,
  onToggleComplete,
  isLoading
}) => {
  // Filter tasks based on the current filter
  const filteredTasks = tasks.filter(task => {
    // Filter by status
    if (filter.status === 'active' && task.completed) return false;
    if (filter.status === 'completed' && !task.completed) return false;

    // Filter by priority
    if (filter.priority && filter.priority !== 'all' && task.priority !== filter.priority) return false;

    // Filter by search term
    if (filter.searchTerm && filter.searchTerm.trim() !== '') {
      const searchTermLower = filter.searchTerm.toLowerCase();
      return (
        task.title.toLowerCase().includes(searchTermLower) ||
        task.description.toLowerCase().includes(searchTermLower)
      );
    }

    return true;
  });

  // Sort the filtered tasks
  const sortedTasks = [...filteredTasks].sort((a, b) => {
    let comparison = 0;
    
    switch (sortOption) {
      case 'title':
        comparison = a.title.localeCompare(b.title);
        break;
      case 'priority': {
        const priorityValues = { high: 3, medium: 2, low: 1 };
        comparison = priorityValues[b.priority] - priorityValues[a.priority];
        break;
      }
      case 'createdAt':
      default:
        comparison = a.createdAt.getTime() - b.createdAt.getTime();
        break;
    }

    return sortDirection === 'asc' ? comparison : -comparison;
  });

  if (isLoading) {
    return (
      <div className="space-y-4 py-8">
        {[...Array(3)].map((_, index) => (
          <div 
            key={index} 
            className="animate-pulse bg-gray-100 p-4 rounded-md h-24"
            aria-hidden="true"
          ></div>
        ))}
        <p className="sr-only">Loading tasks...</p>
      </div>
    );
  }

  if (sortedTasks.length === 0) {
    return (
      <div className="py-12 text-center">
        <svg 
          xmlns="http://www.w3.org/2000/svg" 
          className="mx-auto h-12 w-12 text-gray-400"
          fill="none" 
          viewBox="0 0 24 24" 
          stroke="currentColor"
        >
          <path 
            strokeLinecap="round" 
            strokeLinejoin="round" 
            strokeWidth={1.5} 
            d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" 
          />
        </svg>
        <h3 className="mt-2 text-lg font-medium text-gray-900">No tasks found</h3>
        <p className="mt-1 text-gray-500">
          {filter.status || filter.priority || filter.searchTerm
            ? 'Try changing your filters to see more results.'
            : 'Get started by creating a new task.'}
        </p>
      </div>
    );
  }

  return (
    <div className="mt-4 space-y-2" aria-live="polite">
      {sortedTasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onEdit={onEditTask}
          onDelete={onDeleteTask}
          onToggleComplete={onToggleComplete}
        />
      ))}
    </div>
  );
};

export default TaskList;