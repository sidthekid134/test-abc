import { Task } from '../types/Task';

const TASKS_STORAGE_KEY = 'tasks';

export const getStoredTasks = (): Task[] => {
  const tasksJson = localStorage.getItem(TASKS_STORAGE_KEY);
  if (!tasksJson) return [];

  try {
    const parsedTasks = JSON.parse(tasksJson);
    
    // Convert string dates back to Date objects
    return parsedTasks.map((task: any) => ({
      ...task,
      createdAt: new Date(task.createdAt),
      updatedAt: new Date(task.updatedAt)
    }));
  } catch (error) {
    console.error('Failed to parse tasks from localStorage:', error);
    return [];
  }
};

export const storeTasks = (tasks: Task[]): void => {
  try {
    localStorage.setItem(TASKS_STORAGE_KEY, JSON.stringify(tasks));
  } catch (error) {
    console.error('Failed to store tasks in localStorage:', error);
  }
};

export const addTask = (task: Task): void => {
  const tasks = getStoredTasks();
  storeTasks([...tasks, task]);
};

export const updateTask = (updatedTask: Task): boolean => {
  const tasks = getStoredTasks();
  const taskIndex = tasks.findIndex((task) => task.id === updatedTask.id);
  
  if (taskIndex === -1) return false;
  
  const updatedTasks = [
    ...tasks.slice(0, taskIndex),
    updatedTask,
    ...tasks.slice(taskIndex + 1)
  ];
  
  storeTasks(updatedTasks);
  return true;
};

export const deleteTask = (taskId: string): boolean => {
  const tasks = getStoredTasks();
  const filteredTasks = tasks.filter((task) => task.id !== taskId);
  
  if (filteredTasks.length === tasks.length) return false;
  
  storeTasks(filteredTasks);
  return true;
};