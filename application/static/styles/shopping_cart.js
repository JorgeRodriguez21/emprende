let totalPrice = undefined;
let salePrice = undefined;


function removeElement(idValue) {
    $.ajax({
        type: "PUT",
        url: "/delete",
        // set content type header to use Flask response.get_json()
        contentType: "application/json",
        // convert data/object to JSON to send
        data: JSON.stringify({
            id: idValue
        }),
        success: function (data, status, xhttp) {
            $("#" + idValue).fadeOut("slow", function () {
                $(this).remove();
            });
            setTimeout(function () {
                location.reload()
            }, 500);
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            showErrorMessage(XMLHttpRequest.responseText);
        }
    });

}

function showSuccessMessage(message) {
    let toast = '<div class="toast toast-success">' + message + '</div>';
    $("body").append(toast);
    setTimeout(function () {
        $(".toast").addClass("toast-transition");
    }, 100);
    setTimeout(function () {
        $(".toast").remove();
        location.reload();
        enable_checkout_button();
    }, 3500);
    $(".lightbox-blanket").toggle();
}

function showErrorMessage(message) {
    let toast;
    if (message) {
        toast = "<div class=\"toast toast-error\">" + message + "</div>";
    } else {
        toast = '<div class="toast toast-error">Hubo un error al confirmar la compra</div>';
    }
    $("#app").append(toast);
    setTimeout(function () {
        $(".toast").addClass("toast-transition");
    }, 100);
    setTimeout(function () {
        $(".toast").remove();
        location.reload();
        enable_checkout_button();
    }, 10000);
}

function enable_checkout_button() {
    $("#checkout_button").prop("disabled",false);
}

function disable_checkout_button() {
    $("#checkout_button").prop("disabled",true);
}

function confirmPurchase() {
    disable_checkout_button()
    function getIds() {
        let ids = [];
        $('.price').each(function () {
            let id = $(this).attr('id');
            ids.push(id)
        });
        return ids;
    }
    let address = $("#address")[0].value;

    if (getSelectedLocation() === undefined || getSelectedLocation() === null || address === '' || address === undefined || getIds().length === 0) {
        showErrorMessage("Debe seleccionar una ciudad de entrega y agregar una dirección válida")
    } else {
        $.ajax({
            type: "PUT",
            url: "/confirm",
            // set content type header to use Flask response.get_json()
            contentType: "application/json",
            // convert data/object to JSON to send
            data: JSON.stringify({
                ids: getIds(),
                address,
                city: getSelectedLocation(),
                totalPrice: $('.total').html().substring(1)
            }),
            success: function (data, status, xhttp) {
                let message = 'Su compra fue confirmada correctamente, se le envi&oacute; un email con el detalle de la misma.'
                showSuccessMessage(message);
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                showErrorMessage(XMLHttpRequest.responseText);
            }
        });
    }

}

function confirmOrder(id) {
    $.ajax({
        type: "PUT",
        url: "/order/confirmation",
        // set content type header to use Flask response.get_json()
        contentType: "application/json",
        data: JSON.stringify({
            order: id,
        }),
        // convert data/object to JSON to send
        success: function (data, status, xhttp) {
            let message = 'Orden confirmada.'
            showSuccessMessage(message);
            setTimeout(function () {
                window.location.replace('/orders')
            }, 1000);
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            showErrorMessage(XMLHttpRequest.responseText);
            setTimeout(function () {
                window.location.replace('/orders')
            }, 1000);
        }
    });
}

function cancelOrder(id) {
    $.ajax({
        type: "PUT",
        url: "/order/cancellation",
        // set content type header to use Flask response.get_json()
        contentType: "application/json",
        data: JSON.stringify({
            order: id,
        }),
        // convert data/object to JSON to send
        success: function (data, status, xhttp) {
            let message = 'Orden cancelada.'
            showSuccessMessage(message);
            setTimeout(function () {
                window.location.replace('/orders')
            }, 1000);
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            showErrorMessage(XMLHttpRequest.responseText);
            setTimeout(function () {
                window.location.replace('/orders')
            }, 1000);
        }
    });
}

function calculateSubtotal() {
    let sum = 0;
    const totalUnits = calculateUnitsNumber();
    $('.total_units').html(totalUnits + " unidades en total");
    $('.price').each(function () {
        let counter = $(this).html().substring(1);
        let id = $(this).attr('id');
        sum += parseFloat(counter);
    });
    totalPrice = sum;
    $('.subtotal').html('$' + sum.toFixed(2));
    if(totalUnits>=12) {
        let saleSum = 0;
        $('.price').each(function () {
            let counter = $(this).attr("sale_price")
            let id = $(this).attr('id');
            console.log(counter)
            saleSum += parseFloat(counter);
        });
        salePrice = saleSum;
        const discount = totalPrice - salePrice;
        $('#discount').html('$' + discount.toFixed(2));
    }else {
        salePrice = undefined;
        $('#discount').html('$' + (0.00).toFixed(2));
    }
    calculateTotal();
}

function calculateUnitsNumber() {
    let sum = 0;
    $('.quantity :input').each(function () {
        console.log($(this))
        let counter = $(this).val();
        let id = $(this).attr('id');
        sum += parseInt(counter);
    });
    return sum;
}

function calculateSubtotalForOrders(city) {
    setShippingValue(city)
    const totalUnits = calculateUnitsNumber();
    $('.total_units').html(totalUnits + " unidades en total");
    let sum = 0;
    $('.price').each(function () {
        let counter = $(this).html().substring(1);
        let id = $(this).attr('id');
        sum += parseFloat(counter);
    });
    totalPrice = sum;
    $('.subtotal').html('$' + sum.toFixed(2));
    console.log("!!!!!!!!!!!");
    console.log(totalUnits);
    if(totalUnits>=12) {
        let saleSum = 0;
        $('.price').each(function () {
            let counter = $(this).attr("sale_price")
            console.log(counter);
            let id = $(this).attr('id');
            saleSum += parseFloat(counter);
        });
        salePrice = saleSum;
        const discount = totalPrice - salePrice;
        $('#discount').html('$' + discount.toFixed(2));
    }else {
        salePrice = undefined;
        $('#discount').html('$' + (0.00).toFixed(2));
    }
    calculateTotal();
}

function setShippingValue(city) {
    let value = '5.60'
    if(city === "Quito"){
        value = '3.15';
    }else if(city=== "Cantones y Especiales"){
        value = '6.60'
    }
    let total = parseFloat(value).toFixed(2);
    $('.shipping').html('$' + total);
    calculateTotal();
}

function calculateTotal() {
    let subtotal = parseFloat($('.subtotal').html().substring(1));
    let shipping = parseFloat($('.shipping').html().substring(1));
    let discount = parseFloat($('#discount').html().substring(1));
    let total = subtotal + shipping - discount;
    $('.total').html('$' + total.toFixed(2));
}

function getSelectedLocation() {
    let locationSelector = $("#locationSelector");
    return locationSelector.val();
}

function changeSelection() {
    let shippingValue = '6.60';
    if (getSelectedLocation() === 'Quito') {
        shippingValue = '3.15';
    }else if(getSelectedLocation() === 'Provincias'){
        shippingValue = '5.60';
    }
    let value = parseFloat(shippingValue).toFixed(2);
    $('.shipping').html('$' + value);
    calculateTotal();
}

function goToShopping() {
    window.location.replace("/products");
}
