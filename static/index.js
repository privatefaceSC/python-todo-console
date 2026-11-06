function loadTasks() {
    fetch('http://127.0.0.1:8000/api/tasks')
        .then(response => {
            if (!response.ok) throw new Error('HTTP ' + response.status);
            return response.json();
        })
        .then(tasks => {
            const ulElement = document.getElementById("task-list");
            ulElement.innerHTML = "";

            tasks.forEach((task, index) => {
                const liElement = document.createElement("li");
                liElement.textContent = (task.status ? "✅ " : "❌ ") + task.title;

                const deleteBtn = document.createElement('button');
                deleteBtn.textContent = 'Удалить';
                deleteBtn.addEventListener('click', () => deleteTask(index));

                const statusBtn = document.createElement('button');
                statusBtn.textContent = 'Поменять статус';
                statusBtn.addEventListener('click', () => markTask(index));

                liElement.append(deleteBtn, statusBtn);
                ulElement.appendChild(liElement);
            });
        })
        .catch(error => console.error('Ошибка загрузки:', error));
}

function addTask() {
    const inputElement = document.getElementById("task-input");
    const taskTitle = inputElement.value;

    if (!taskTitle.trim()) {
        alert("Введите название задачи!");
        return;
    }

    fetch('http://127.0.0.1:8000/api/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: taskTitle })
    })
        .then(response => {
            if (!response.ok) throw new Error('HTTP ' + response.status);
            inputElement.value = "";
            loadTasks();
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert("Не удалось добавить задачу");
        });
}

function deleteTask(index) {
    fetch(`http://127.0.0.1:8000/tasks/${index}`, {
        method: 'DELETE'
    })
        .then(response => {
            if (!response.ok) throw new Error('HTTP ' + response.status);
            loadTasks();
        })
        .catch(error => console.error('Ошибка удаления:', error));
}
function markTask(index) {
    fetch(`http://127.0.0.1:8000/tasks/${index}`, {
        method: 'PATCH'
    })
        .then(response => {
            if (!response.ok) throw new Error('HTTP ' + response.status);
            loadTasks();
        })
        .catch(error => console.error('Ошибка удаления:', error));
}
loadTasks();