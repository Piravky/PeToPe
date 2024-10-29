document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('click', function() {
      this.classList.toggle('clicked');
    });
  });

