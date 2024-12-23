document.getElementById('registration-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Предотвращаем отправку формы по умолчанию

    const username = document.getElementById('username').value.trim(); // Изменено с username на name
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value.trim();

    // Проверка обязательных полей
    if (!username || !email || !password) {
        alert('Пожалуйста, заполните все поля.');
        return;
    }

    // Создаем объект с данными для отправки
    const data = {
        id: 0, // Устанавливаем id на 0, если сервер это позволяет
        name: username,
        email: email,
        password: password,
        score_cat: 0, // Добавляем score_cat
        score_dog: 0  // Добавляем score_dog
    };


    // Отправляем POST-запрос на сервер
    fetch(IP_API + '/api/v1/users/', {
        method: 'POST',
        headers: {
            accept: 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {

            return response.json().then(err => { throw new Error(err.message || 'Ошибка сети'); });
            
        }
        return response.json();
    })


    .then(data => {
        console.log('Успех:', data);
        alert("вы успешно зарегистрировались")
        // window.location.href = "../html/login.html"
        window.location.href = "/login"
        // Здесь можно добавить логику для перехода на другую страницу или отображения сообщения
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Ошибка: ' + error.message);
        alert("возможно такой пользователь уже существует");
    });
});
