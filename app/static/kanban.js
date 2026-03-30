// Kanban Board Drag-and-Drop Functionality
document.addEventListener('DOMContentLoaded', function() {
  const tasks = document.querySelectorAll('.kanban-task');
  const taskLists = document.querySelectorAll('.kanban-tasks');

  let draggedTask = null;
  let sourceStatus = null;

  // Make tasks draggable
  tasks.forEach(task => {
    task.addEventListener('dragstart', handleDragStart);
    task.addEventListener('dragend', handleDragEnd);
  });

  // Make drop zones draggable
  taskLists.forEach(list => {
    list.addEventListener('dragover', handleDragOver);
    list.addEventListener('drop', handleDrop);
    list.addEventListener('dragleave', handleDragLeave);
  });

  function handleDragStart(e) {
    draggedTask = this;
    sourceStatus = this.getAttribute('data-status');
    this.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/html', this.innerHTML);
  }

  function handleDragEnd(e) {
    this.classList.remove('dragging');

    // Remove drag-over class from all lists
    taskLists.forEach(list => {
      list.classList.remove('drag-over');
    });
  }

  function handleDragOver(e) {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    this.closest('.kanban-tasks').classList.add('drag-over');
    return false;
  }

  function handleDragLeave(e) {
    // Only remove if we're leaving the tasks list entirely
    if (e.target === this) {
      this.classList.remove('drag-over');
    }
  }

  function handleDrop(e) {
    e.preventDefault();
    e.stopPropagation();

    const tasksList = this;
    const targetStatus = tasksList.getAttribute('data-status');

    if (draggedTask && sourceStatus !== targetStatus) {
      const taskId = draggedTask.getAttribute('data-task-id');

      // Optimistically update UI
      draggedTask.setAttribute('data-status', targetStatus);
      tasksList.appendChild(draggedTask);

      // Update status on server
      updateTaskStatus(taskId, targetStatus, draggedTask, sourceStatus);
    }

    this.classList.remove('drag-over');
    return false;
  }

  function updateTaskStatus(taskId, newStatus, taskElement, previousStatus) {
    const url = `/${taskId}/status`;
    const payload = {
      status: newStatus
    };

    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload)
    })
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      console.log('Task status updated successfully:', data);
      showNotification('Task moved to ' + newStatus, 'success');
    })
    .catch(error => {
      console.error('Error updating task status:', error);
      showNotification('Error updating task. Please try again.', 'error');

      // Revert the change
      taskElement.setAttribute('data-status', previousStatus);
      const previousList = document.querySelector(`.kanban-tasks[data-status="${previousStatus}"]`);
      if (previousList) {
        previousList.appendChild(taskElement);
      }
    });
  }

  function showNotification(message, type = 'info') {
    // Create a simple toast notification
    const notification = document.createElement('div');
    notification.style.cssText = `
      position: fixed;
      bottom: 2rem;
      right: 2rem;
      background: ${type === 'success' ? '#10b981' : '#ef4444'};
      color: white;
      padding: 1rem 1.5rem;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
      font-weight: 500;
      z-index: 1000;
      animation: slideUp 0.3s ease;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);

    // Remove after 3 seconds
    setTimeout(() => {
      notification.style.animation = 'slideDown 0.3s ease';
      setTimeout(() => notification.remove(), 300);
    }, 3000);
  }
});

// Add animation styles
const style = document.createElement('style');
style.textContent = `
  @keyframes slideUp {
    from {
      transform: translateY(100px);
      opacity: 0;
    }
    to {
      transform: translateY(0);
      opacity: 1;
    }
  }

  @keyframes slideDown {
    from {
      transform: translateY(0);
      opacity: 1;
    }
    to {
      transform: translateY(100px);
      opacity: 0;
    }
  }
`;
document.head.appendChild(style);
