document.addEventListener("DOMContentLoaded", function () {
  // Obtener la hora actual del sistema
  var horaActual = new Date().getHours();

  // Verificar si la hora es impar
  if (horaActual % 2 !== 0) {
    // Construir la URL completa a nueva_ventana.html
    var nuevaVentanaURL = "{% url 'nueva_ventana' %}";
    
    // Abrir la nueva ventana
    window.open(nuevaVentanaURL, "_blank");
  }
});
