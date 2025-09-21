import { Task } from '../types';
import { TaskCard } from './TaskCard';
import { useTaskContext } from '../contexts/TaskContext';

interface TaskListProps {
  tasks?: Task[];
}

export const TaskList = ({ tasks }: TaskListProps) => {
  const { filteredTasks, isLoading } = useTaskContext();
  
  // Use the passed tasks or the filtered tasks from context
  const tasksToRender = tasks || filteredTasks;

  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (tasksToRender.length === 0) {
    return (
      <div className="bg-white rounded-lg p-6 text-center shadow-sm">
        <p className="text-gray-500">No tasks found</p>
      </div>
    );
  }

  return (
    <div className="mt-4">
      {tasksToRender.map((task) => (
        <TaskCard key={task.id} task={task} />
      ))}
    </div>
  );
};