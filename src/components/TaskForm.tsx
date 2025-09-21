import { useState, FormEvent } from 'react';
import { TaskFormData, Task, TaskPriority, TaskStatus } from '../types';
import { Input } from './Input';
import { Textarea } from './Textarea';
import { Select } from './Select';
import { Button } from './Button';
import { useTaskContext } from '../contexts/TaskContext';

interface TaskFormProps {
  task?: Task;
  onSubmit?: () => void;
  onCancel?: () => void;
}

const initialFormState: TaskFormData = {
  title: '',
  description: '',
  status: 'pending',
  priority: 'medium',
};

const statusOptions = [
  { value: 'pending', label: 'Pending' },
  { value: 'in-progress', label: 'In Progress' },
  { value: 'completed', label: 'Completed' },
];

const priorityOptions = [
  { value: 'low', label: 'Low' },
  { value: 'medium', label: 'Medium' },
  { value: 'high', label: 'High' },
];

export const TaskForm = ({ task, onSubmit, onCancel }: TaskFormProps) => {
  const { addTask, updateTask } = useTaskContext();
  
  const [formData, setFormData] = useState<TaskFormData>(
    task
      ? {
          title: task.title,
          description: task.description,
          status: task.status,
          priority: task.priority,
        }
      : initialFormState
  );
  
  const [errors, setErrors] = useState<Partial<TaskFormData>>({});

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    
    // Clear error when field is edited
    if (errors[name as keyof TaskFormData]) {
      setErrors((prev) => ({ ...prev, [name]: undefined }));
    }
  };

  const validateForm = (): boolean => {
    const newErrors: Partial<TaskFormData> = {};
    
    if (!formData.title.trim()) {
      newErrors.title = 'Title is required';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) return;

    if (task) {
      updateTask(task.id, formData);
    } else {
      addTask(formData);
      setFormData(initialFormState);
    }
    
    if (onSubmit) onSubmit();
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-4 rounded-md shadow-sm">
      <Input
        id="task-title"
        name="title"
        label="Title"
        value={formData.title}
        onChange={handleChange}
        placeholder="Enter task title"
        error={errors.title}
        fullWidth
        required
        aria-required="true"
      />
      
      <Textarea
        id="task-description"
        name="description"
        label="Description"
        value={formData.description}
        onChange={handleChange}
        placeholder="Enter task description"
        rows={3}
        fullWidth
      />
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Select
          id="task-status"
          name="status"
          label="Status"
          value={formData.status}
          onChange={handleChange}
          options={statusOptions}
          fullWidth
        />
        
        <Select
          id="task-priority"
          name="priority"
          label="Priority"
          value={formData.priority}
          onChange={handleChange}
          options={priorityOptions}
          fullWidth
        />
      </div>
      
      <div className="flex justify-end space-x-2 mt-4">
        {onCancel && (
          <Button
            type="button"
            variant="secondary"
            onClick={onCancel}
          >
            Cancel
          </Button>
        )}
        
        <Button type="submit" variant="primary">
          {task ? 'Update Task' : 'Create Task'}
        </Button>
      </div>
    </form>
  );
};