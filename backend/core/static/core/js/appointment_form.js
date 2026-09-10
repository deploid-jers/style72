console.log("Appointment JS loaded!");

document.addEventListener("DOMContentLoaded", function () {
    const typeField = document.getElementById("id_type");

    const fields = [
        "id_specialist",
        "id_service",
        "id_appointment_date",
        "id_appointment_time",
    ];

    function toggleBookingFields() {
        const isOnlineBooking = typeField.value === "online_booking";

        fields.forEach(function (fieldId) {
            const field = document.getElementById(fieldId);

            if (!field) return;

            field.closest(".form-row").style.display =
                isOnlineBooking ? "" : "none";
        });
    }

    typeField.addEventListener("change", toggleBookingFields);

    toggleBookingFields();
});