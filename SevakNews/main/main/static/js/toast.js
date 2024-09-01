function closeAlert(button) {
  var alert = button.parentNode.parentNode;
  alert.classList.remove('show');
  alert.style.opacity = 0;
  setTimeout(function() {
      alert.style.display = 'none';
  }, 300);
}

var alerts = document.querySelectorAll('.alert');
alerts.forEach(function(alert) {
  setTimeout(function() {
      closeAlert(alert.querySelector('.btn-close'));
  }, 10000);
});