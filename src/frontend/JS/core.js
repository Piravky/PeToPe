document.querySelectorAll('.btn').forEach(button => {
  button.addEventListener('click', function () {
    // Удаление класса 'clicked' с других кнопок
    document.querySelectorAll('.btn.clicked').forEach(btn => {
      btn.classList.remove('clicked');
    });
    this.classList.add('clicked'); // Добавление класса 'clicked' к нажатой кнопке
  });
});

function drawQuestions(data) {
  console.log(data); // Обработка полученных данных
  console.log('Вопрос ' + data[0]["id"])
  console.log(data[0]["question"]);
  for (let i = 0; i < data[1].length; i++) {
    console.log(data[1][i]["answer"]);
  }


  const form = document.getElementById('catForm');

  // Создаем элемент для вопроса
  const questionLabel = document.createElement('label');
  questionLabel.textContent = 'Вопрос ' + data[0]["id"] + '. ' + data[0]["question"];
  form.appendChild(questionLabel);
  form.appendChild(document.createElement('br')); // Добавляем перенос строки

  // Создаем элементы для ответов
  data[1].forEach(answer => {
    const button = document.createElement('button');
    button.textContent = answer['answer'];
    button.className = 'answer-button';
    button.type = 'button'; // Устанавливаем тип кнопки как 'button'\
    form.appendChild(document.createElement('br')); // Добавляем перенос строки

    // Добавляем обработчик события для кнопки
    button.addEventListener('click', function () {
      alert('Вы выбрали: ' + answer.answer);
    });

    // Добавляем кнопку в форму
    form.appendChild(button);
  });

  // Добавляем кнопку отправки
  const submitButton = document.createElement('input');
  submitButton.type = 'submit';
  submitButton.value = 'Далее';
  form.appendChild(submitButton);

  // Обработчик события для формы
  form.addEventListener('submit', function (event) {
    event.preventDefault(); // Предотвращаем стандартное поведение отправки формы
    alert('Форма отправлена.');
  });


}


// создание функции в JavaScript
function Jmak() {

  url = "";
  ip = "192.168.0.21" // Каждый раз надо писать новый IP

  const button_cat = document.getElementById('id_button_cat');
  const button_dog = document.getElementById('id_button_dog');

  if (button_cat.classList.contains('clicked')) {
    url = 'http://' + ip + ':8001/cat/question/1'
  }
  else if (button_dog.classList.contains('clicked')) {
    url = 'http://' + ip + ':8001/dog/question/1'
  }
  else {
    alert("Не выбрано животное");
    return;
  }

  // alert("Жмак");
  fetch(url, {})
    .then(response => {
      if (response.ok) {
        return response.json(); // Если CORS настроен правильно, мы можем получить данные
      } else {
        throw new Error('Network response was not ok');
      }
    })
    .then(d => {
      drawQuestions(d);
    })
    .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
    });



}








