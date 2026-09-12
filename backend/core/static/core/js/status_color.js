(function () {
    // Карта цветов: Укажите ВАШИ значения из choices в models.py (в нижнем или верхнем регистре)
    const statusColors = {
        'new': { bg: '#e4fd00', text: '#464646' },         
        'confirmed': { bg: '#0f9fff', text: 'rgb(253, 253, 253)' },
        'cancelled': { bg: '#ff0000', text: '#fff5f5' }, 
        'completed': { bg: '#17ff0f', text: 'rgb(49, 49, 49)' },  
        
        'NEW': { bg: '#e4fd00', text: '#464646' },
        'CONFIRMED': { bg: '#0f9fff', text: 'rgb(253, 253, 253)' },
        'CANCELLED': { bg: '#ff0000', text: '#fff5f5' },
        'COMPLETED': { bg: '#17ff0f', text: 'rgb(49, 49, 49)' }
    };

    function applyStatusStyles() {
        const selects = document.querySelectorAll('table select');

        selects.forEach(select => {
            const val = select.value;
            const config = statusColors[val];

            if (config) {
                // 1. Красим сам select
                select.style.backgroundColor = config.bg;
                select.style.color = config.text;
                select.style.fontWeight = 'bold';
                select.style.borderRadius = '6px';
                select.style.padding = '4px 8px';

                // 2. Красим родительский контейнер Select2 (костыль для Unfold)
                const select2Container = select.nextElementSibling;
                if (select2Container && select2Container.classList.contains('select2-container')) {
                    const selection = select2Container.querySelector('.select2-selection');
                    if (selection) {
                        selection.style.backgroundColor = config.bg;
                        selection.style.color = config.text;
                        selection.style.borderRadius = '6px';
                    }
                }
            }
        });
    }

    // Запускаем окрашивание с задержкой, чтобы Unfold успел проинициализировать стили
    window.addEventListener('load', function () {
        applyStatusStyles();

        // Перехватываем изменения селектов
        document.addEventListener('change', function (e) {
            if (e.target && e.target.tagName === 'SELECT') {
                applyStatusStyles();
            }
        });

        // Слушаем события Select2 (если Unfold перехватил выбор)
        if (window.jQuery) {
            window.jQuery('table select').on('change.select2', function () {
                applyStatusStyles();
            });
        }
    });
})();