document.addEventListener('DOMContentLoaded', function() {
    console.log('Initializing Kanban board...');
    
    let draggedCard = null;
    let originalColumn = null;
    
    // Get the current job ID from the URL
    const currentPath = window.location.pathname;
    const jobIdMatch = currentPath.match(/\/jobs\/(\d+)\/applicants\/?/);
    const jobId = jobIdMatch ? jobIdMatch[1] : null;
    
    console.log('Current job ID:', jobId);

    // Make all application cards draggable
    const applicationCards = document.querySelectorAll('.application-card');
    console.log(`Found ${applicationCards.length} application cards`);
    
    applicationCards.forEach(card => {
        card.addEventListener('dragstart', function(e) {
            console.log('Drag started for card:', this.dataset.applicationId);
            draggedCard = this;
            originalColumn = this.closest('.kanban-column');
            this.classList.add('dragging');
            e.dataTransfer.effectAllowed = 'move';
            e.dataTransfer.setData('text/plain', this.dataset.applicationId);
        });

        card.addEventListener('dragend', function(e) {
            console.log('Drag ended');
            this.classList.remove('dragging');
            document.querySelectorAll('.kanban-column').forEach(col => {
                col.classList.remove('drag-over');
            });
        });
    });

    // Setup drop zones for all columns
    const kanbanColumns = document.querySelectorAll('.kanban-column');
    console.log(`Found ${kanbanColumns.length} kanban columns`);
    
    kanbanColumns.forEach(column => {
        column.addEventListener('dragover', function(e) {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'move';
        });

        column.addEventListener('dragenter', function(e) {
            e.preventDefault();
            this.classList.add('drag-over');
        });

        column.addEventListener('dragleave', function(e) {
            if (!this.contains(e.relatedTarget)) {
                this.classList.remove('drag-over');
            }
        });

        column.addEventListener('drop', function(e) {
            e.preventDefault();
            console.log('Drop event on column:', this.dataset.stage);
            
            this.classList.remove('drag-over');
            
            if (!draggedCard || !jobId) {
                console.error('Missing job ID or dragged card');
                showNotification('Error: Cannot move application', 'error');
                return;
            }

            const applicationId = e.dataTransfer.getData('text/plain');
            const newStage = this.dataset.stage;
            
            // Check if this is the same column
            if (this === originalColumn) {
                console.log('Dropped in same column, ignoring');
                return;
            }
            
            console.log(`Moving application ${applicationId} to stage ${newStage}`);
            
            // Store the current state for potential rollback
            const currentState = {
                applicationId: applicationId,
                oldColumn: originalColumn,
                newColumn: this,
                draggedCard: draggedCard
            };
            
            // Send AJAX request first, then update UI on success
            updateApplicationStage(jobId, applicationId, newStage, currentState);
        });
    });

    function updateColumnCounts() {
        document.querySelectorAll('.kanban-column').forEach(column => {
            const applicationsList = column.querySelector('.applications-list');
            const cards = applicationsList.querySelectorAll('.application-card');
            const countElement = column.querySelector('.application-count');
            countElement.textContent = cards.length;
            
            const existingEmptyMsg = applicationsList.querySelector('.empty-column');
            if (cards.length === 0 && !existingEmptyMsg) {
                applicationsList.innerHTML = '<div class="empty-column text-center text-gray-500 py-8"><p>No applicants in this stage</p></div>';
            }
        });
    }

    function updateApplicationStage(jobId, applicationId, newStage, currentState) {
        const csrfToken = getCookie('csrftoken');
        const url = `/jobs/${jobId}/applicants/update-stage/`;
        
        console.log('Making request to:', url);
        console.log('Application ID:', applicationId);
        console.log('New stage:', newStage);
        
        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `application_id=${applicationId}&stage=${newStage}`
        })
        .then(response => {
            console.log('Response status:', response.status);
            console.log('Response headers:', response.headers);
            
            if (!response.ok) {
                // Try to get error message from response
                return response.text().then(text => {
                    throw new Error(`HTTP error! status: ${response.status}, response: ${text}`);
                });
            }
            return response.json();
        })
        .then(data => {
            console.log('Response data:', data);
            
            if (data.success) {
                // Update UI only after successful backend update
                moveCardVisually(currentState);
                updateColumnCounts();
                showNotification(`✓ Moved to ${data.new_stage_name}`, 'success');
                
                // Reset for next drag operation
                draggedCard = null;
                originalColumn = null;
            } else {
                showNotification(`❌ Error: ${data.error}`, 'error');
                // Don't revert since we haven't updated UI yet
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('❌ Error moving application. Check console for details.', 'error');
            console.log('Full error details:', error);
        });
    }

    function moveCardVisually(currentState) {
        const applicationsList = currentState.newColumn.querySelector('.applications-list');
        applicationsList.appendChild(currentState.draggedCard);
        
        // Remove empty message if it exists
        const emptyMsg = applicationsList.querySelector('.empty-column');
        if (emptyMsg) {
            emptyMsg.remove();
        }
    }

    function showNotification(message, type) {
        // Remove any existing notifications
        const existingNotifications = document.querySelectorAll('.kanban-notification');
        existingNotifications.forEach(notification => notification.remove());
        
        const notification = document.createElement('div');
        notification.className = `kanban-notification fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg ${
            type === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
        }`;
        notification.textContent = message;
        notification.style.transition = 'all 0.3s ease';
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.style.opacity = '1';
        }, 10);
        
        setTimeout(() => {
            notification.style.opacity = '0';
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    console.log('Kanban board initialized successfully!');
});