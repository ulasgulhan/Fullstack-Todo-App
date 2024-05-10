
function submitRegisterForm() {
    var username = document.getElementById("registerUsername").value;
    fetch("/auth/register/", {
        method: 'POST',
        body: JSON.stringify({username: username}),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (response.status === 204) {
            getLoginAfterRegister()
            document.getElementById("registerError").style.display = "none";
            console.log(response.error, response.statusText)
        } else if (response.status === 406) {
            response.json().then(data => {
                document.getElementById("registerError").innerText = data.error;
                document.getElementById("registerError").style.display = "block";
                document.getElementById('registerSuccess').style.display = 'none'; 
                
            });
        } else {
            console.error('Error:', response.statusText);
        }
    });
    return false;
}


document.body.addEventListener('htmx:afterRequest', (event) => {
    fetchActiveTasks()
    document.querySelector("input[name='task']").value = '';
});


document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.querySelector("#registerForm");
    if (registerForm) {
        registerForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            try {
                await getLoginAfterRegister();
            } catch (error) {
                console.error('Error:', error);
            }
        });
    } else {
        console.error("Element with ID 'registerForm' not found.");
    }
});


function reloadPage() {
    setTimeout(() => {
        location.reload();
    }, 1500);
}


function getLoginAfterRegister() {
    console.log("getLoginAfterRegister function called");
    document.getElementById('registerForm').style.display = 'none';
    document.getElementById('registerSuccess').style.display = 'block'; 
    setTimeout(() => { showLoginForm(); }, 1500); 
}


function fetchTasks(url) {
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const tasksContainer = document.getElementById('task-list');
            const tasksCountContainer = document.getElementById('task-count');
            tasksContainer.innerHTML = '';
            tasksCountContainer.innerHTML = `Active Tasks: ${data.active_task_count}`;
            data.tasks.forEach(task => {
                const taskDiv = document.createElement('div');
                taskDiv.classList.add('flex', 'items-center', 'space-x-4', 'flex', 'flex-wrap', 'whitespace-normal', 'break-all', 'justify-between', 'w-full', 'bg-white', 'hover:bg-[#F8F7F7]', 'border-[#EDEAE9]', 'border-b');

                const completeButton = document.createElement('button');
                completeButton.innerHTML = '&#10004;';
                completeButton.classList.add('text-[#363639]', 'border-2', 'border-[#363639]', 'rounded-full', 'w-7', 'h-7', 'flex', 'justify-center', 'hover:bg-[#E6F8F1]', 'hover:border-[#60A688]', 'hover:text-[#60A688]', 'ml-4');
                if (task.is_complete) {
                    completeButton.classList.remove('border-[#363639]');
                    completeButton.classList.add('bg-[#E6F8F1]', 'border-[#60A688]', 'text-[#60A688]', 'hover:bg-transparent', 'hover:border-[#363639]', 'hover:text-[#363639]');
                }
                completeButton.addEventListener('click', () => {
                    if (!task.is_complete) {
                        patchTaskComplete(task.id)
                            .then(() => {
                                fetchActiveTasks();
                                completeButton.classList.add('bg-[#1EBB8C]', 'text-white');
                            });
                    } else {
                        patchTaskComplete(task.id)
                            .then(() => {
                                fetchCompletedTasks();
                                completeButton.classList.remove('bg-[#1EBB8C]', 'text-white');
                            });
                    }
                });

                const taskElement = document.createElement('p');
                taskElement.textContent = task.task;
                taskElement.classList.add('text-left', 'flex-grow', 'max-w-[calc(100%-14rem)]', 'flex', 'items-center', 'min-h-16');
                if (task.is_complete) {
                    taskElement.style.textDecoration = 'line-through';
                    taskElement.style.color = 'text-[#363639]';
                }

                taskElement.addEventListener('dblclick', () => {
                    const editableTaskElement = document.createElement('input');
                    editableTaskElement.type = 'text';
                    editableTaskElement.value = task.task;
                    editableTaskElement.classList.add('flex-grow', 'mb-2', 'px-4', 'py-2', 'border', 'rounded');
                    
                    editableTaskElement.addEventListener('blur', () => {
                        const updatedTask = editableTaskElement.value.trim();
                        if (updatedTask !== task.task) {
                            patchTaskUpdate(task.id, updatedTask)
                                .then(() => fetchActiveTasks());
                        }
                        taskDiv.replaceChild(taskElement, editableTaskElement);
                    });
                
                    editableTaskElement.addEventListener('keydown', (event) => {
                        if (event.key === 'Enter') {
                            editableTaskElement.blur();
                        }
                    });
                
                    taskDiv.replaceChild(editableTaskElement, taskElement);
                    editableTaskElement.focus();
                });

                const deleteButton = document.createElement('button');
                deleteButton.innerHTML = '&#10006; &nbsp; Delete';
                deleteButton.classList.add('hover:text-[#D93256]', 'text-[#EB7586]', 'font-bold', 'py-2', 'px-4', 'rounded');
                deleteButton.addEventListener('click', () => {
                    if (task.is_complete) {
                        patchTaskDelete(task.id);
                        tasksContainer.removeChild(taskDiv);
                    } else {
                        patchTaskDelete(task.id);
                        tasksContainer.removeChild(taskDiv);
                        data.active_task_count -= 1;
                        tasksCountContainer.innerHTML = `Active Tasks: ${data.active_task_count}`;
                    }
                });

                const hr = document.createElement('hr');
                hr.classList.add('border', 'border-[#EDEAE9]');

                taskDiv.appendChild(completeButton);
                taskDiv.appendChild(taskElement);
                taskDiv.appendChild(deleteButton);
                taskDiv.appendChild(hr);

                tasksContainer.appendChild(taskDiv);


            });
        });
}


function patchTaskDelete(taskId) {
    fetch(`/api/tasks/delete/${taskId}`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        console.log('Task patched successfully');
    })
    .catch(error => {
        console.error('There was a problem with the patch request:', error);
    });
}


function patchTaskComplete(taskId) {
    return fetch(`/api/tasks/complete/${taskId}`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        console.log('Task patched successfully');
    })
    .catch(error => {
        console.error('There was a problem with the patch request:', error);
    });
}


function patchTaskUpdate(taskId, updatedTask) {
    return fetch(`/api/tasks/update/${taskId}`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ task: updatedTask })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        console.log('Task updated successfully');
    })
    .catch(error => {
        console.error('There was a problem with the patch request:', error);
    });
}


function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}


function showLoginForm() {
    document.getElementById('formTitle').innerText = 'Login to your account';
    document.getElementById('loginForm').style.display = 'block';
    document.getElementById('registerForm').style.display = 'none';
    document.getElementById('registerSuccess').style.display = 'none';
}


function loginSuccess(){
    document.getElementById('loginForm').style.display = 'none';
    document.getElementById('loginSuccess').style.display = 'block';
}


function showRegisterForm() {
    document.getElementById('formTitle').innerText = 'Create an account';
    document.getElementById('loginForm').style.display = 'none';
    document.getElementById('registerForm').style.display = 'block';
    document.getElementById('registerSuccess').style.display = 'none';
    document.getElementById('registerError').style.display = 'none';
}


function fetchCompletedTasks() {
    fetchTasks('/api/tasks/completed/');
    document.getElementById('completedTasksBtn').classList.add('bg-[#2BA470]', 'text-white');
    document.getElementById('completedTasksBtn').classList.remove('text-black');
    document.getElementById('activeTasksBtn').classList.remove('bg-[#3C46FF]', 'text-white');
    document.getElementById('activeTasksBtn').classList.add('text-black');
}


function fetchActiveTasks() {
    fetchTasks('/api/tasks/active');
    document.getElementById('activeTasksBtn').classList.add('bg-[#3C46FF]', 'text-white');
    document.getElementById('activeTasksBtn').classList.remove('text-black');
    document.getElementById('completedTasksBtn').classList.remove('bg-[#2BA470]', 'text-white');
    document.getElementById('completedTasksBtn').classList.add('text-black');
}


window.addEventListener('load', fetchActiveTasks);
