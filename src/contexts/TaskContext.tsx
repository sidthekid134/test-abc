import { createContext, useContext, ReactNode, useReducer, useEffect } from 'react';
import { Task, TaskFormData, TaskFilters, SortOption } from '../types';
import { v4 as uuidv4 } from 'uuid';

// Define context types
interface TaskContextType {
  tasks: Task[];
  filteredTasks: Task[];
  isLoading: boolean;
  error: string | null;
  filters: TaskFilters;
  sortOption: SortOption;
  addTask: (task: TaskFormData) => void;
  updateTask: (id: string, task: Partial<TaskFormData>) => void;
  deleteTask: (id: string) => void;
  setFilters: (filters: TaskFilters) => void;
  setSortOption: (sortOption: SortOption) => void;
  clearFilters: () => void;
}

// Create context with default values
const TaskContext = createContext<TaskContextType | undefined>(undefined);

// Action types
type TaskAction =
  | { type: 'LOAD_TASKS_START' }
  | { type: 'LOAD_TASKS_SUCCESS'; payload: Task[] }
  | { type: 'LOAD_TASKS_ERROR'; payload: string }
  | { type: 'ADD_TASK'; payload: Task }
  | { type: 'UPDATE_TASK'; payload: { id: string; task: Partial<TaskFormData> } }
  | { type: 'DELETE_TASK'; payload: string }
  | { type: 'SET_FILTERS'; payload: TaskFilters }
  | { type: 'SET_SORT_OPTION'; payload: SortOption }
  | { type: 'CLEAR_FILTERS' };

// Initial state
interface TaskState {
  tasks: Task[];
  filteredTasks: Task[];
  isLoading: boolean;
  error: string | null;
  filters: TaskFilters;
  sortOption: SortOption;
}

const initialState: TaskState = {
  tasks: [],
  filteredTasks: [],
  isLoading: false,
  error: null,
  filters: {},
  sortOption: { field: 'createdAt', direction: 'desc' },
};

// Helper function to filter and sort tasks
const filterAndSortTasks = (
  tasks: Task[],
  filters: TaskFilters,
  sortOption: SortOption
): Task[] => {
  // First filter
  let filteredTasks = [...tasks];

  if (filters.status) {
    filteredTasks = filteredTasks.filter((task) => task.status === filters.status);
  }

  if (filters.priority) {
    filteredTasks = filteredTasks.filter((task) => task.priority === filters.priority);
  }

  if (filters.searchTerm) {
    const searchTerm = filters.searchTerm.toLowerCase();
    filteredTasks = filteredTasks.filter(
      (task) =>
        task.title.toLowerCase().includes(searchTerm) ||
        task.description.toLowerCase().includes(searchTerm)
    );
  }

  // Then sort
  return filteredTasks.sort((a, b) => {
    const { field, direction } = sortOption;
    
    if (field === 'title') {
      return direction === 'asc'
        ? a.title.localeCompare(b.title)
        : b.title.localeCompare(a.title);
    }
    
    if (field === 'priority') {
      const priorityOrder = { low: 0, medium: 1, high: 2 };
      const aValue = priorityOrder[a.priority];
      const bValue = priorityOrder[b.priority];
      return direction === 'asc' ? aValue - bValue : bValue - aValue;
    }
    
    if (field === 'status') {
      const statusOrder = { 'pending': 0, 'in-progress': 1, 'completed': 2 };
      const aValue = statusOrder[a.status as keyof typeof statusOrder];
      const bValue = statusOrder[b.status as keyof typeof statusOrder];
      return direction === 'asc' ? aValue - bValue : bValue - aValue;
    }
    
    // For dates (createdAt, updatedAt)
    const aDate = field === 'createdAt' ? a.createdAt : a.updatedAt;
    const bDate = field === 'createdAt' ? b.createdAt : b.updatedAt;
    
    return direction === 'asc'
      ? new Date(aDate).getTime() - new Date(bDate).getTime()
      : new Date(bDate).getTime() - new Date(aDate).getTime();
  });
};

// Reducer function
const taskReducer = (state: TaskState, action: TaskAction): TaskState => {
  switch (action.type) {
    case 'LOAD_TASKS_START':
      return { ...state, isLoading: true, error: null };
    
    case 'LOAD_TASKS_SUCCESS':
      return {
        ...state,
        tasks: action.payload,
        filteredTasks: filterAndSortTasks(action.payload, state.filters, state.sortOption),
        isLoading: false,
      };
    
    case 'LOAD_TASKS_ERROR':
      return { ...state, isLoading: false, error: action.payload };
    
    case 'ADD_TASK':
      const updatedTasks = [...state.tasks, action.payload];
      return {
        ...state,
        tasks: updatedTasks,
        filteredTasks: filterAndSortTasks(updatedTasks, state.filters, state.sortOption),
      };
    
    case 'UPDATE_TASK':
      const { id, task } = action.payload;
      const updatedTaskList = state.tasks.map((t) =>
        t.id === id
          ? { ...t, ...task, updatedAt: new Date() }
          : t
      );
      return {
        ...state,
        tasks: updatedTaskList,
        filteredTasks: filterAndSortTasks(updatedTaskList, state.filters, state.sortOption),
      };
    
    case 'DELETE_TASK':
      const filteredTasks = state.tasks.filter((t) => t.id !== action.payload);
      return {
        ...state,
        tasks: filteredTasks,
        filteredTasks: filterAndSortTasks(filteredTasks, state.filters, state.sortOption),
      };
    
    case 'SET_FILTERS':
      return {
        ...state,
        filters: action.payload,
        filteredTasks: filterAndSortTasks(state.tasks, action.payload, state.sortOption),
      };
    
    case 'SET_SORT_OPTION':
      return {
        ...state,
        sortOption: action.payload,
        filteredTasks: filterAndSortTasks(state.tasks, state.filters, action.payload),
      };
    
    case 'CLEAR_FILTERS':
      return {
        ...state,
        filters: {},
        filteredTasks: filterAndSortTasks(state.tasks, {}, state.sortOption),
      };
    
    default:
      return state;
  }
};

// Provider component
interface TaskProviderProps {
  children: ReactNode;
}

export const TaskProvider = ({ children }: TaskProviderProps) => {
  const [state, dispatch] = useReducer(taskReducer, initialState);

  // Load tasks from localStorage on initial render
  useEffect(() => {
    const loadTasks = async () => {
      dispatch({ type: 'LOAD_TASKS_START' });
      
      try {
        const storedTasks = localStorage.getItem('tasks');
        if (storedTasks) {
          // Parse stored JSON and convert string dates to Date objects
          const parsedTasks = JSON.parse(storedTasks).map((task: any) => ({
            ...task,
            createdAt: new Date(task.createdAt),
            updatedAt: new Date(task.updatedAt),
          }));
          dispatch({ type: 'LOAD_TASKS_SUCCESS', payload: parsedTasks });
        } else {
          dispatch({ type: 'LOAD_TASKS_SUCCESS', payload: [] });
        }
      } catch (error) {
        dispatch({ type: 'LOAD_TASKS_ERROR', payload: 'Failed to load tasks' });
      }
    };

    loadTasks();
  }, []);

  // Save tasks to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem('tasks', JSON.stringify(state.tasks));
  }, [state.tasks]);

  // Task operations
  const addTask = (taskData: TaskFormData) => {
    const now = new Date();
    const newTask: Task = {
      id: uuidv4(),
      ...taskData,
      createdAt: now,
      updatedAt: now,
    };
    
    dispatch({ type: 'ADD_TASK', payload: newTask });
  };

  const updateTask = (id: string, taskData: Partial<TaskFormData>) => {
    dispatch({ type: 'UPDATE_TASK', payload: { id, task: taskData } });
  };

  const deleteTask = (id: string) => {
    dispatch({ type: 'DELETE_TASK', payload: id });
  };

  // Filter and sort operations
  const setFilters = (filters: TaskFilters) => {
    dispatch({ type: 'SET_FILTERS', payload: filters });
  };

  const setSortOption = (sortOption: SortOption) => {
    dispatch({ type: 'SET_SORT_OPTION', payload: sortOption });
  };

  const clearFilters = () => {
    dispatch({ type: 'CLEAR_FILTERS' });
  };

  const value = {
    ...state,
    addTask,
    updateTask,
    deleteTask,
    setFilters,
    setSortOption,
    clearFilters,
  };

  return <TaskContext.Provider value={value}>{children}</TaskContext.Provider>;
};

// Custom hook for using the context
export const useTaskContext = (): TaskContextType => {
  const context = useContext(TaskContext);
  if (context === undefined) {
    throw new Error('useTaskContext must be used within a TaskProvider');
  }
  return context;
};