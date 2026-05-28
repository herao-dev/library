/**
 * 图书管理系统 - 自定义脚本
 */

function confirmAction(message, actionUrl) {
    document.getElementById('confirmMessage').textContent = message;
    document.getElementById('confirmForm').action = actionUrl;
    var modal = new bootstrap.Modal(document.getElementById('confirmModal'));
    modal.show();
}

document.addEventListener('DOMContentLoaded', function () {
    setTimeout(function () {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function (alert) {
            var bsAlert = new bootstrap.Alert(alert);
            setTimeout(function () {
                bsAlert.close();
            }, 5000);
        });
    }, 0);
});