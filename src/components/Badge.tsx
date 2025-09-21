import { ReactNode } from 'react';
import { TaskPriority, TaskStatus } from '../types';

interface BadgeProps {
  children: ReactNode;
  variant: 'status' | 'priority';
  value: TaskStatus | TaskPriority;
}

export const Badge = ({ children, variant, value }: BadgeProps) => {
  const baseClasses = 'px-2 py-1 rounded-full text-xs font-medium';
  
  const getStatusClasses = (status: TaskStatus) => {
    switch (status) {
      case 'pending':
        return 'bg-gray-200 text-gray-800';
      case 'in-progress':
        return 'bg-blue-100 text-blue-800';
      case 'completed':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };
  
  const getPriorityClasses = (priority: TaskPriority) => {
    switch (priority) {
      case 'low':
        return 'bg-gray-100 text-gray-800';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'high':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };
  
  const variantClasses = variant === 'status' 
    ? getStatusClasses(value as TaskStatus) 
    : getPriorityClasses(value as TaskPriority);

  return (
    <span className={`${baseClasses} ${variantClasses}`}>
      {children}
    </span>
  );
};