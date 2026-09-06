document.addEventListener('DOMContentLoaded', () => {
    
    // 1. Плавный скролл по якорным ссылкам меню
    const links = document.querySelectorAll('.nav-list a');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80, // минус высота шапки
                    behavior: 'smooth'
                });
            }
        });
    });

    // 2. Обработка отправки формы (имитация)
    const form = document.getElementById('contactForm');
    form.addEventListener('submit', (e) => {
        e.preventDefault(); // Останавливаем перезагрузку страницы
        alert('Спасибо! Ваша заявка успешно отправлена. Мы свяжемся с вами в течение 15 минут.');
        form.reset(); // Очищаем поля формы
    });

    // 3. Открытие мобильного меню (Базовая логика для доработки)
    const burger = document.getElementById('burger');
    const nav = document.getElementById('nav');

    burger.addEventListener('click', () => {
        // Если мобильное меню скрыто - показываем, и наоборот
        if (nav.style.display === 'block') {
            nav.style.display = 'none';
        } else {
            nav.style.display = 'block';
            nav.style.position = 'absolute';
            nav.style.top = '80px';
            nav.style.left = '0';
            nav.style.width = '100%';
            nav.style.backgroundColor = '#fff';
            nav.style.padding = '20px';
            nav.style.boxShadow = '0 10px 10px rgba(0,0,0,0.1)';
        }
    });
});