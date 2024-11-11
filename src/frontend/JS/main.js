let currentQ = 1;
document.getElementById('get-questions').onclick = async function () {
    const animalType = document.getElementById('animal-type').value;
    currentQ = 1;
    renderQuestions(animalType);
};


function renderQuestions(animalType) {
    const container = document.getElementById('questions-container');
    container.innerHTML = ''; // Очищаем контейнер перед добавлением новых вопросов
    const url = 'http://212.20.53.168:8080/' + animalType + '/question/';
    const url_send = 'http://212.20.53.168:8080/users/' + animalType + '/sum_scores/1?answer_id='
    fetch(url + currentQ.toString())
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Network response was not ok');
            }
        })
        .then(data => {
            const questionDiv = document.createElement('div');
            questionDiv.innerHTML = `<p>${'Вопрос ' + data[0]["id"] + '. ' + data[0]["question"]}</p>`;
            container.appendChild(questionDiv);
            container.appendChild(document.createElement('br'));
            data[1].forEach(answer => {
                const button = document.createElement('button');
                button.textContent = answer['answer'];
                button.className = 'answer-button';
                button.type = 'button'; // Устанавливаем тип кнопки как 'button'
                container.appendChild(document.createElement('br')); // Добавляем перенос строки

                // Добавляем обработчик события для кнопки
                button.addEventListener('click', function () {
                    currentQ += 1
                    const response = fetch(url_send + answer.id.toString(), { // Замените на ваш URL
                        method: 'POST', // Метод запроса
                        headers: {
                            'Content-Type': 'application/json', // Указываем тип контента
                        },
                        body: JSON.stringify(data) // Преобразуем объект в JSON-строку
                    });
                    renderQuestions(animalType);

                });
                // Добавляем кнопку в форму
                container.appendChild(button);
            }); // Вызов функции с полученными данными
        })
        .catch(error => {
            currentQ = 1;
            handleAnswer(animalType)
        });

    // questions.forEach(question => {
    //     const questionDiv = document.createElement('div');
    //     questionDiv.innerHTML = `<p>${question.text}</p>`;
    //     question.options.forEach(option => {
    //         const button = document.createElement('button');
    //         button.textContent = option;
    //         button.onclick = () => handleAnswer(question.id, option);
    //         questionDiv.appendChild(button);
    //     });
    //     container.appendChild(questionDiv);
    // });
}

function handleAnswer(animalType) {
    const container = document.getElementById('result');
    container.innerHTML = ''; 
    const url = 'http://212.20.53.168:8080/users/1/' + animalType + '_breed/';
    fetch(url)
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Network response was not ok');
            }
        })
        .then(data => {
            console.log(data)
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML += `<p>Порода ${data.breed}: ${data.description}"</p>`;
            container.appendChild(resultDiv);

        })

    // Здесь можно добавить логику для определения породы на основе ответов
}