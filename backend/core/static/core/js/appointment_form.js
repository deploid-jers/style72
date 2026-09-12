document.addEventListener("DOMContentLoaded", function () {
    const $ = django.jQuery; // Используем jQuery от Django Admin

    const typeField = document.getElementById("id_type");
    const fields = [
        "id_specialist",
        "id_service",
        "id_appointment_date",
        "id_appointment_time",
    ];

    function toggleBookingFields() {
        if (!typeField) return;
        const isOnlineBooking = typeField.value === "online_booking";

        fields.forEach(function (fieldId) {
            const field = document.getElementById(fieldId);
            if (!field) return;
            
            // Находим строку формы
            const formRow = field.closest(".form-row");
            if (formRow) {
                formRow.style.display = isOnlineBooking ? "" : "none";
            }
        });
    }

    function loadSpecialistServices() {
        const specialistId = $("#id_specialist").val();
        const $serviceField = $("#id_service");

        // Если специалист не выбран
        if (!specialistId) {
            $serviceField.empty().append(new Option("---------", ""));
            $serviceField.trigger("change"); // Уведомляем Select2
            return;
        }

        fetch(`/admin/api/specialists/${specialistId}/services/`)
            .then(response => {
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                return response.json();
            })
            .then(services => {
                // Запоминаем текущее выбранное значение (если оно было)
                const currentSelected = $serviceField.val();

                // Очищаем существующие варианты
                $serviceField.empty();
                $serviceField.append(new Option("---------", ""));

                // Наполняем новыми опциями
                services.forEach(service => {
                    const newOption = new Option(service.name, service.id, false, false);
                    $serviceField.append(newOption);
                });

                // Если предыдущее значение есть в новом списке — сохраняем его
                if (currentSelected && $serviceField.find(`option[value="${currentSelected}"]`).length) {
                    $serviceField.val(currentSelected);
                } else {
                    $serviceField.val("");
                }

                // ВАЖНО: Уведомляем Select2, что <select> обновился
                $serviceField.trigger("change.select2");
            })
            .catch(error => {
                console.error("FETCH ERROR:", error);
            });
    }

    if (typeField) {
        typeField.addEventListener("change", toggleBookingFields);
    }

    // Вешаем событие change через django.jQuery
    $(document).on("change", "#id_specialist", loadSpecialistServices);

    toggleBookingFields();
});