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

async function defineVisibility() {
    return await $.ajax({
        sync: false,
        async: true,
        type: "GET",
        url: "/roles",
        dataType: 'json',
        success: function (data, status, xhttp) {
            const isAdmin = data['isAdmin']
            const isLogged = data['isLogged']
            console.log(isAdmin)
            console.log(isLogged)
            if(isAdmin && isAdmin===true){
                $("#products").show()
                $("#orders").show()
            }
            if (isLogged && isLogged===true){
                $("#btnSession").html("Cerrar Sesión")
            }else{
                $("#btnSession").html("Iniciar Sesión")
            }
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            console.log(XMLHttpRequest.responseText)
        }
    });
}
function isUserLogged() {
    $.ajax({
        type: "GET",
        url: "/manage_session",
        dataType: 'json',
        success: function (data, status, xhttp) {
            if (data){
                window.location.replace("/");
            }else{
                window.location.replace("/login");
            }
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            window.location.replace("/products");
        }
    });
}