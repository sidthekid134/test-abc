import { useState } from 'react';
import { Task } from '../types';
import { Badge } from './Badge';
import { Button } from './Button';
import { TaskForm } from './TaskForm';
import { useTaskContext } from '../contexts/TaskContext';

interface TaskCardProps {
  task: Task;
}

export const TaskCard = ({ task }: TaskCardProps) => {
  const { deleteTask } = useTaskContext();
  const [isEditing, setIsEditing] = useState(false);
  const [showConfirmDelete, setShowConfirmDelete] = useState(false);

  const handleEditClick = () => {
    setIsEditing(true);
  };

  const handleEditCancel = () => {
    setIsEditing(false);
  };

  const handleEditSubmit = () => {
    setIsEditing(false);
  };

  const handleDeleteClick = () => {
    setShowConfirmDelete(true);
  };

  const handleDeleteConfirm = () => {
    deleteTask(task.id);
    setShowConfirmDelete(false);
  };

  const handleDeleteCancel = () => {
    setShowConfirmDelete(false);
  };

  // Format dates to be more readable
  const formattedCreatedDate = new Date(task.createdAt).toLocaleDateString();
  const formattedUpdatedDate = new Date(task.updatedAt).toLocaleDateString();

  if (isEditing) {
    return (
      <div className="border rounded-lg p-4 mb-4 bg-white shadow-sm">
        <h3 className="text-lg font-medium mb-3">Edit Task</h3>
        <TaskForm 
          task={task} 
          onSubmit={handleEditSubmit} 
          onCancel={handleEditCancel} 
        />
      </div>
    );
  }

  return (
    <div className="border rounded-lg p-4 mb-4 bg-white shadow-sm">
      <div className="flex justify-between items-start mb-2">
        <h3 className="text-lg font-medium">{task.title}</h3>
        <div className="flex space-x-2">
          <Badge variant="status" value={task.status}>
            {task.status.replace('-', ' ')}
          </Badge>
          <Badge variant="priority" value={task.priority}>
            {task.priority}
          </Badge>
        </div>
      </div>
      
      <p className="text-gray-600 mb-4">{task.description || 'No description'}</p>
      
      <div className="text-xs text-gray-500 mb-4">
        <div>Created: {formattedCreatedDate}</div>
        <div>Last Updated: {formattedUpdatedDate}</div>
      </div>
      
      {showConfirmDelete ? (
        <div className="border-t pt-3 mt-2">
          <p className="text-sm text-gray-700 mb-2">Are you sure you want to delete this task?</p>
          <div className="flex space-x-2">
            <Button variant="danger" size="sm" onClick={handleDeleteConfirm}>
              Delete
            </Button>
            <Button variant="secondary" size="sm" onClick={handleDeleteCancel}>
              Cancel
            </Button>
          </div>
        </div>
      ) : (
        <div className="flex justify-end space-x-2 border-t pt-3 mt-2">
          <Button variant="secondary" size="sm" onClick={handleEditClick}>
            Edit
          </Button>
          <Button variant="danger" size="sm" onClick={handleDeleteClick}>
            Delete
          </Button>
        </div>
      )}
    </div>
  );
};