export type TaskStatus = 'pending' | 'in-progress' | 'completed';

export type TaskPriority = 'low' | 'medium' | 'high';

export interface Task {
  id: string;
  title: string;
  description: string;
  status: TaskStatus;
  priority: TaskPriority;
  createdAt: Date;
  updatedAt: Date;
}

export interface TaskFormData {
  title: string;
  description: string;
  status: TaskStatus;
  priority: TaskPriority;
}

export interface TaskFilters {
  status?: TaskStatus;
  priority?: TaskPriority;
  searchTerm?: string;
}

export interface SortOption {
  field: 'title' | 'createdAt' | 'updatedAt' | 'priority' | 'status';
  direction: 'asc' | 'desc';
}