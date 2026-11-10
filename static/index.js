async function loadTasks() {
    try {
        const response = await fetch('/api/tasks')
        if (!response.ok) throw new Error('HTTP ' + response.status);
        const tasks = await response.json();

        const ulElement = document.getElementById("task-list");
        ulElement.innerHTML = "";

        tasks.forEach((task) => {
            const liElement = document.createElement("li");
            liElement.textContent = (task.status ? "✅ " : "❌ ") + task.title;

            const deleteBtn = document.createElement('button');
            deleteBtn.textContent = 'Удалить';
            deleteBtn.addEventListener('click', async () => await deleteTask(task.id));

            const statusBtn = document.createElement('button');
            statusBtn.textContent = 'Поменять статус';
            statusBtn.addEventListener('click', async () => await markTask(task.id));

            liElement.append(deleteBtn, statusBtn);
            ulElement.appendChild(liElement);
        });
    } catch(error) {
    console.error('Ошибка загрузки:', error);}
}

async function addTask() {
    const inputElement = document.getElementById("task-input");
    const taskTitle = inputElement.value;

    if (!taskTitle.trim()) {
        alert("Введите название задачи!");
        return;
    }

    try {

        const response = await fetch('/api/tasks', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({title: taskTitle})
        });
        if (!response.ok) throw new Error('HTTP ' + response.status);
        inputElement.value = "";
        await loadTasks();

    } catch(error) {
        console.error('Ошибка:', error);
        alert("Не удалось добавить задачу");
    }
}

async function deleteTask(id) {
    try {
        const response = await fetch(`/api/tasks/${id}`, {
            method: 'DELETE'
        });
        if (!response.ok) throw new Error('HTTP ' + response.status);
        await loadTasks();

    } catch(error) {
        console.error('Ошибка удаления:', error);
    }
}
async function markTask(id) {
    try {
        const response = await fetch(`/api/tasks/${id}`, {
            method: 'PATCH'
        })
        if (!response.ok) throw new Error('HTTP ' + response.status);
        await loadTasks();
    } catch(error) {
    console.error('Ошибка смены статуса:', error);
    }
}
loadTasks();