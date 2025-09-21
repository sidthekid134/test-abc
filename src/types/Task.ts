export interface Task {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  priority: 'low' | 'medium' | 'high';
  createdAt: Date;
  updatedAt: Date;
}

export type TaskFormData = Omit<Task, 'id' | 'createdAt' | 'updatedAt'>;

export type TaskFilter = {
  status?: 'all' | 'active' | 'completed';
  priority?: 'all' | 'low' | 'medium' | 'high';
  searchTerm?: string;
};

export type SortOption = 'createdAt' | 'priority' | 'title';
export type SortDirection = 'asc' | 'desc';