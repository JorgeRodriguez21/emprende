function showSuccessMessage(message) {
    let toast = '<div class="toast toast-success">' + message + '</div>';
    $("body").append(toast);
    setTimeout(function () {
        $(".toast").addClass("toast-transition");
    }, 100);
    setTimeout(function () {
        $(".toast").remove();
    }, 3500);
    $(".lightbox-blanket").toggle();
}

function showErrorMessage(message) {
    let toast;
    if (message) {
        toast = "<div class=\"toast toast-error\">" + message + "</div>";
    } else {
        toast = '<div class="toast toast-error">Hubo un error al almacenar los productos</div>';
    }
    $("body").append(toast);
    setTimeout(function () {
        $(".toast").addClass("toast-transition");
    }, 100);
    setTimeout(function () {
        $(".toast").remove();
    }, 3500);
    console.log(message);
}