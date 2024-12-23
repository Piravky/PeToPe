token = localStorage.getItem('access_token');
let currentQ = 1;
let selectedAnimalType = null; // Переменная для хранения выбранного типа животного

function checkAuthorization() {
    // Здесь мы предполагаем, что информация об авторизации хранится в localStorag

    if (!token) {
        alert('Вы не авторизованы. Переход на страницу входа.');
        window.location.href = '/login'; // Укажите путь к странице входа
    } else {
        // Здесь можно добавить код для отображения контента страницы
        console.log('Пользователь авторизован. Страница загружена.');
    }
}
window.onload = checkAuthorization;

// Обработчик клика для кнопок выбора животного
document.querySelectorAll('.animal-button').forEach(button => {
    button.onclick = function() {
        selectedAnimalType = this.value; // Сохраняем выбранный тип животного
    };
});

// Обработчик клика для кнопки "Получить вопросы"
document.getElementById('get-questions').onclick = async function () {
    if (!selectedAnimalType) return; // Если тип животного не выбран, ничего не делаем
    currentQ = 1;
    const start = document.getElementById('start');
    start.innerHTML = '';
    renderQuestions(selectedAnimalType);
};

function renderQuestions(animalType) {
    const container = document.getElementById('questions-container');
    container.innerHTML = ''; // Очищаем контейнер перед добавлением новых вопросов
    container.style.display = 'flex'; // Используем Flexbox
    container.style.justifyContent = 'center'; // Центрируем по горизонтали
    container.style.flexDirection = 'column'; // Располагаем кнопки в колонку
    container.style.alignItems = 'center'; // Центрируем по вертикали
    const url = IP_API + '/api/v1/' + animalType + '/question/';
    const url_send = IP_API + '/api/v1/users/' + animalType + '/sum_scores?answer_id=';
    fetch(url + currentQ.toString(), {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        },
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Network response was not ok');
            }
        })
        .then(data => {
            const questionDiv = document.createElement('div');
            questionDiv.innerHTML = `<h4 class="text-center">${'Вопрос ' + data[0]["id"] + '</h4><h2 class="text-center">' + data[0]["question"]}</h2>`;
            questionDiv.style.display = 'flex'; // Используем Flexbox
            questionDiv.style.justifyContent = 'center'; // Центрируем по горизонтали
            questionDiv.style.flexDirection = 'column'; // Располагаем кнопки в колонку
            questionDiv.style.alignItems = 'center'; // Центрируем по вертикали
            container.appendChild(questionDiv);
            // container.appendChild(document.createElement('br'));
            data[1].forEach(answer => {
                const button = document.createElement('button');
                button.textContent = answer['answer'];
                button.className = 'answer-button Knopka-border m-1 p-2 px-3 Knopka text-center';
                button.type = 'button'; // Устанавливаем тип кнопки как 'button'

                // Добавляем обработчик события для кнопки
                button.addEventListener('click', function () {
                    currentQ += 1;
                    const response = fetch(url_send + answer.id.toString(), { // Замените на ваш URL
                        method: 'POST', // Метод запроса
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': 'Bearer ' + token // Указываем тип контента
                        },
                        body: JSON.stringify(data) // Преобразуем объект в JSON-строку
                    });

                    renderQuestions(animalType);
                });
                // Добавляем кнопку в форму
                container.appendChild(button);
            });
        })
        .catch(error => {
            currentQ = 1;
            handleAnswer(animalType);
        });
}

function handleAnswer(animalType) {
    const container = document.getElementById('result');
    container.innerHTML = '';
    const url = IP_API + '/api/v1/users/' + animalType + '_breed';
    fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        }
    })
        .then(response => {
            if (response.ok) {
		console.log(response)
                return response.json();
            } else {
                throw new Error('Network response was not ok');
            }
        })
        .then(data => {
            console.log(data);
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML += `
            <div class="container m-3 mx-auto">
                <div class="row featurette align-items-center justify-content-center">
                    <div class="col-md-7">
                        <h2 class="featurette-heading fw-normal lh-1">${data[0].breed}</h2>
                        <p class="lead opacity-75">${data[0].breed} — ${data[0].description}</p>
                        <div class="btn-toolbar">
                            <button id = "testagain" type="button" class="btn btn-light me-2 btn-lg">Пройти тест заново</button>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <img src="${data[0].image}" class="img-fluid rounded-4" alt="Проба">
                    </div>
                </div>
            </div>
            `;
            document.getElementById('testagain').addEventListener('click', function() {
                fetch(IP_API + '/api/v1/users/score_none', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + token
                    },
                    body: JSON.stringify({})
                })
                .then(response => {
                    if (response.ok) {
                        location.reload(true);
                    } else {
                        console.error('Ошибка при выходе');
                    }
                })
                .catch(error => {
                    console.error('Ошибка сети:', error);
                });
            });

        });
}

document.getElementById('logoutButton').addEventListener('click', function() {
    fetch(IP_API + '/api/v1/users/score_none', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
        },
        body: JSON.stringify({})
    })
    .then(response => {
        if (response.ok) {
            localStorage.clear();
            window.location.href = '/login'; // Замените на нужный URL
        } else {
            console.error('Ошибка при выходе');
        }
    })
    .catch(error => {
        console.error('Ошибка сети:', error);
    });
});

document.querySelectorAll('.Knopka').forEach(button => {
    button.addEventListener('click', function () {
      // Удаление класса 'clicked' с других кнопок
      document.querySelectorAll('.Knopka.clicked').forEach(btn => {
        btn.classList.remove('clicked');
      });
      this.classList.add('clicked'); // Добавление класса 'clicked' к нажатой кнопке
    });
  });

