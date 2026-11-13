async function Register() {
    const input_emailElement = document.getElementById("email-input");
    const emailTitle = input_emailElement.value;
    const input_passwordElement = document.getElementById("password-input");
    const passwordTitle = input_passwordElement.value;


    if (!emailTitle.trim()) {
        alert("Введите почту");
        return;
    }
    if (!passwordTitle.trim()) {
        alert("Введите пароль");
        return;
    }

    try {
        const response = await fetch('/api/registration', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({email: emailTitle.trim(), password: passwordTitle})
        });

        if (!response.ok) {
            // Если сервер говорит, что email занят (400)
            if (response.status === 400) {
                alert("Пользователь с таким email уже существует");
                return; // Выходим, чтобы не перекидывать на /tasks
            }
            // Если другая ошибка (500, 404 и т.д.)
            throw new Error('HTTP ' + response.status);
        }

        const data = await response.json();
        localStorage.setItem('access_token', data.access_token);
        window.location.href = '/tasks';

    } catch (error) {
        console.error('Ошибка:', error);
        alert("Не удалось зарегистрироваться");
    }
}