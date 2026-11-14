const token = localStorage.getItem('access_token')
if (!token) {
    window.location.href = '/';
}
async function loadTasks() {
    try {
            const response = await fetchWithAuth('/load/tasks', {
            headers: {'Content-Type': 'application/json'
        }
    });
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

        const response = await fetchWithAuth('/add/tasks', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({title: taskTitle.trim()})
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
        const response = await fetchWithAuth(`/delete/tasks/${id}`, {
            method: 'DELETE',
            headers: {'Content-Type': 'application/json'}
        });

        if (!response.ok) throw new Error('HTTP ' + response.status);
        await loadTasks();

    } catch(error) {
        console.error('Ошибка удаления:', error);
    }
}
async function markTask(id) {
    try {
        const response = await fetchWithAuth(`/change/status/tasks/${id}`, {
            method: 'PATCH',
            headers: {'Content-Type': 'application/json'}
        });
        if (!response.ok) throw new Error('HTTP ' + response.status);
        await loadTasks();
    } catch(error) {
    console.error('Ошибка смены статуса:', error);
    }
}

async function fetchWithAuth(url, options = {}) {
    // 1. Берем текущий Access Token
    let token = localStorage.getItem('access_token');

    // Добавляем заголовок Authorization
    options.headers = {
        ...options.headers,
        'Authorization': 'Bearer ' + token
    };

    // 2. Делаем запрос
    let response = await fetch(url, options);

    // 3. Если токен умер (401)
    if (response.status === 401) {
        console.log("Access Token умер. Пробуем обновить...");
        // Просто стучимся на /refresh. Браузер САМ прикрепит куки!
        const refreshResponse = await fetch('/refresh/token/validation', { method: 'POST' });

        // 4. Если Refresh тоже умер
        if (!refreshResponse.ok) {
            localStorage.clear(); // Удаляем все токены
            window.location.href = '/';
            throw new Error("Сессия истекла");
        }

        // 5. Если Refresh жив — сохраняем новые токены
        const data = await refreshResponse.json();
        localStorage.setItem('access_token', data.access_token);
        // localStorage.setItem('refresh_token', data.refresh_token);

        // 6. Повторяем исходный запрос с НОВЫМ токеном
        options.headers['Authorization'] = 'Bearer ' + data.access_token;
        response = await fetch(url, options);
    }

    return response;
}
loadTasks();