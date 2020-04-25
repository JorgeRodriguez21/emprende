function navigateToAddProduct() {
    window.location.replace("/register_product");
}

function navigateToInventory() {
    window.location.replace("/find_products");
}

function navigateToOrders() {
    window.location.replace("/orders");
}

function navigateToShoppingCart() {
    window.location.replace("/my_cart");
}

function isUserLogged() {
    $.ajax({
        type: "GET",
        url: "/manage_session",
        dataType: 'json',
        success: function (data, status, xhttp) {
            if (data) {
                window.location.replace("/");
            } else {
                window.location.replace("/login");
            }
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            window.location.replace("/products");
        }
    });
}