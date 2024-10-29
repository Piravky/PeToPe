document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('click', function() {
      // Удаление класса 'clicked' с других кнопок
      document.querySelectorAll('.btn.clicked').forEach(btn => {
        btn.classList.remove('clicked');
      });
      this.classList.add('clicked'); // Добавление класса 'clicked' к нажатой кнопке
    });
  });

  