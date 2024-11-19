// Обработчик кнопок
document.querySelectorAll('.btn').forEach(button => {
  button.addEventListener('click', function () {
    // Удаление класса 'clicked' с других кнопок
    document.querySelectorAll('.btn.clicked').forEach(btn => {
      btn.classList.remove('clicked');
    });
    this.classList.add('clicked'); // Добавление класса 'clicked' к нажатой кнопке
  });
});

// Функция для отображения вопросов и ответов
function drawQuestions(data) {
  console.log(data); // Обработка полученных данных
  console.log('Вопрос ' + data[0]["id"]);
  console.log(data[0]["question"]);
  
  const form = document.getElementById('catForm');
  form.innerHTML = ''; // Очищаем форму перед добавлением новых элементов

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
    button.type = 'button'; // Устанавливаем тип кнопки как 'button'
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

var countQuestions = 0;
// Функция Jmak для получения данных и перехода на новую страницу
function Jmak() {
  let url = "";
  const ip = "10.22.202.111"; // IP адрес
  
  

  const button_cat = document.getElementById('id_button_cat');
  const button_dog = document.getElementById('id_button_dog');

  if (button_cat.classList.contains('clicked')) {
    url = 'http://' + ip + ':8001/cat/question/';
    countQuestions = 12
  } else if (button_dog.classList.contains('clicked')) {
    url = 'http://' + ip + ':8001/dog/question/';
    countQuestions = 18;
  } else {
    alert("Не выбрано животное");
    return;
  }
  

  // Сохраняем URL в localStorage
  localStorage.setItem('questionUrl', url);

  // Переход на новую страницу
  window.location.href = 'newPage.html'; // Замените 'newPage.html' на нужный URL
}

// Проверка на новой странице
if (window.location.pathname.includes('newPage.html')) {
  const url = localStorage.getItem('questionUrl');

  if (url) {
    for (let i = 1; i <= 13; i++) {
      new_url = url + i.toString()
      console.log(new_url)
      fetch(new_url)
        .then(response => {
          if (response.ok) {
            return response.json();
          } else {
            throw new Error('Network response was not ok');
          }
        })
        .then(data => {
          drawQuestions(data); // Вызов функции с полученными данными
        })
        .catch(error => {
          console.error('Проблема с операцией fetch:', error);
        });
    }
  } else {
    console.error('URL не найден в localStorage');
  }
}
