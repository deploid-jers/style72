document.addEventListener("DOMContentLoaded", function () {
    const timeInputs = document.querySelectorAll('input[type="time"], .vTimeField');
    
    timeInputs.forEach(input => {
        input.type = 'text'; 
        
        flatpickr(input, {
            enableTime: true,
            noCalendar: true,
            dateFormat: "H:i",     
            time_24hr: true,      
            minuteIncrement: 15,  
        });
    });
});