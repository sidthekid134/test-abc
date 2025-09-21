import React from 'react';
import { TaskFilter as FilterType, SortOption, SortDirection } from '../types/Task';

interface TaskFilterProps {
  filter: FilterType;
  sortOption: SortOption;
  sortDirection: SortDirection;
  onFilterChange: (filter: FilterType) => void;
  onSortChange: (option: SortOption) => void;
  onSortDirectionChange: (direction: SortDirection) => void;
}

const TaskFilter: React.FC<TaskFilterProps> = ({
  filter,
  sortOption,
  sortDirection,
  onFilterChange,
  onSortChange,
  onSortDirectionChange
}) => {
  const handleStatusChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onFilterChange({
      ...filter,
      status: e.target.value as 'all' | 'active' | 'completed'
    });
  };

  const handlePriorityChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onFilterChange({
      ...filter,
      priority: e.target.value as 'all' | 'low' | 'medium' | 'high'
    });
  };

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onFilterChange({
      ...filter,
      searchTerm: e.target.value
    });
  };

  const handleSortChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    onSortChange(e.target.value as SortOption);
  };

  const toggleSortDirection = () => {
    onSortDirectionChange(sortDirection === 'asc' ? 'desc' : 'asc');
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow-sm border mb-6">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0 md:space-x-4">
        {/* Search input */}
        <div className="flex-1">
          <label htmlFor="searchTerm" className="sr-only">Search tasks</label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <input
              type="text"
              id="searchTerm"
              name="searchTerm"
              value={filter.searchTerm || ''}
              onChange={handleSearchChange}
              className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              placeholder="Search tasks..."
              aria-label="Search tasks"
            />
          </div>
        </div>

        <div className="flex flex-wrap gap-2">
          {/* Status filter */}
          <div className="flex-shrink-0">
            <label htmlFor="status" className="sr-only">Filter by status</label>
            <select
              id="status"
              name="status"
              value={filter.status || 'all'}
              onChange={handleStatusChange}
              className="block w-full pl-3 pr-10 py-2 text-base border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              aria-label="Filter by status"
            >
              <option value="all">All Tasks</option>
              <option value="active">Active</option>
              <option value="completed">Completed</option>
            </select>
          </div>

          {/* Priority filter */}
          <div className="flex-shrink-0">
            <label htmlFor="priority" className="sr-only">Filter by priority</label>
            <select
              id="priority"
              name="priority"
              value={filter.priority || 'all'}
              onChange={handlePriorityChange}
              className="block w-full pl-3 pr-10 py-2 text-base border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              aria-label="Filter by priority"
            >
              <option value="all">All Priorities</option>
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>
          
          {/* Sort options */}
          <div className="flex items-center space-x-2">
            <select
              id="sortOption"
              name="sortOption"
              value={sortOption}
              onChange={handleSortChange}
              className="block w-full pl-3 pr-10 py-2 text-base border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              aria-label="Sort by"
            >
              <option value="createdAt">Date Created</option>
              <option value="priority">Priority</option>
              <option value="title">Title</option>
            </select>
            
            <button 
              onClick={toggleSortDirection}
              className="p-2 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              aria-label={`Sort ${sortDirection === 'asc' ? 'ascending' : 'descending'}`}
            >
              {sortDirection === 'asc' ? (
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4h13M3 8h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12" />
                </svg>
              ) : (
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4h13M3 8h9m-9 4h9m5-4v12m0 0l-4-4m4 4l4-4" />
                </svg>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TaskFilter;