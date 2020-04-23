let maxValue = undefined;
let idValue = undefined;
let totalPrice = undefined;
let title = undefined;
let image_name=undefined

function OpenProduct(id, colors, sizes, image_name_param) {
    idValue = id;
    image_name = image_name_param
    //Load image
    let image = $('.product_image[item-data="' + id + '"] img');
    let lbi = $('.lightbox-blanket .product-image img');
    $(lbi).attr("src", $(image).attr("src"));
    //Load unit price
    let unit_price = $('.product_unit_price[item-data="' + id + '"] span').text().substring(1).split('.');
    let dollars = unit_price[0].match(/\d+/)[0];
    let cents = unit_price[1] ? unit_price[1].match(/\d+/)[0] : undefined;
    if (cents === undefined) {
        cents = '00'
    } else if (cents.length === 0) {
        cents = '00'
    } else if (cents.length === 1) {
        cents = cents + '0'
    }
    let dialogPrice = $('.lightbox-blanket .product-info .product-price');
    $(dialogPrice).html("$" + dollars + "<span class='product-price-cents'>" + cents + "</span>");
    //Load sale price
    let sale_price = $('.product_sale_price[item-data="' + id + '"] span').text().substring(1).split('.');
    let sale_dollars = sale_price[0].match(/\d+/)[0];
    let sale_cents = sale_price[1] ? sale_price[1].match(/\d+/)[0] : undefined;
    if (sale_cents === undefined) {
        sale_cents = '00'
    } else if (sale_cents.length === 0) {
        sale_cents = '00'
    } else if (sale_cents.length === 1) {
        sale_cents = sale_cents + '0'
    }
    let dialogSalePrice = $('.lightbox-blanket .product-info .product-price-sale');
    $(dialogSalePrice).html("$" + sale_dollars + "<span class='product-price-cents'>" + sale_cents + "</span>"
        + "<span class='product-price' style='font-size:0.7em'>&nbsp; por docena</span>");
    //Load title
    title = $('.product_title[item-data="' + id + '"] h5').text();
    let dialogTitle = $('.lightbox-blanket .product-title');
    $(dialogTitle).html(title);
    //Load description
    let description = $('.product_desc[item-data="' + id + '"]').text();
    let dialogDescription = $('.lightbox-blanket .product-description');
    $(dialogDescription).html(description);
    //Load available units
    let available_units = $('.product_available_price[item-data="' + id + '"] span[item-data="' + id + '"]').text();
    maxValue = parseInt(available_units);
    let dialogAvailableUnits = $('.lightbox-blanket .product-available');
    $(dialogAvailableUnits).html(available_units + ' Unidades disponibles');

    $(".lightbox-blanket").toggle();

    createSizesSelector(sizes);
    createColorSelector(colors);

    $("#product-quantity-input").val("0");
    CalcPrice(0);
}

function GoBack() {
    $(".lightbox-blanket").toggle();
}

function GetMax() {
    return maxValue;
}

//Calculate new total when the quantity changes.
function CalcPrice(units) {
    let unit_price = $('.product_unit_price[item-data="' + idValue + '"] span').attr('price-data');
    let sale_price = $('.product_sale_price[item-data="' + idValue + '"] span').attr('price-data');
    totalPrice = units >= 12 ? parseFloat((sale_price * units)).toFixed(2) : parseFloat((unit_price * units)).toFixed(2);
    $(".product-checkout-total-amount").text(totalPrice);
}

//Reduce quantity by 1 if clicked
$(document).on("click", ".product-quantity-subtract", function (e) {
    let value = $("#product-quantity-input").val();
    let newValue = parseInt(value) - 1;
    if (newValue < 0) newValue = 0;
    if (newValue > GetMax()) newValue = GetMax();
    $("#product-quantity-input").val(newValue);
    CalcPrice(newValue);
});

//Increase quantity by 1 if clicked
$(document).on("click", ".product-quantity-add", function (e) {
    let value = $("#product-quantity-input").val();
    let newValue = parseInt(value) + 1;
    if (newValue > GetMax()) newValue = GetMax();
    $("#product-quantity-input").val(newValue);
    CalcPrice(newValue);
});

$(document).on("blur", "#product-quantity-input", function (e) {
    var value = $("#product-quantity-input").val();
    CalcPrice(value);
});

function createColorSelector(values) {
    let valueArray = values.split(",");
    let colorSelector = $("#colorSelector");
    colorSelector.html("");
    if (valueArray.length > 0) {
        colorSelector.append("<option selected disabled hidden>Seleccione un color ...</option>");
    }

    valueArray.forEach(value =>
        colorSelector.append("<option value=\"" + value + "\">" + value + "</option>")
    )
}

function createSizesSelector(values) {
    let valueArray = values.split(",");
    let sizeSelector = $("#sizeSelector");
    sizeSelector.html("");
    if (valueArray.length > 0) {
        sizeSelector.append("<option selected disabled hidden>Seleccione la talla ...</option>");
    }
    valueArray.forEach(value =>
        sizeSelector.append("<option value=\"" + value + "\">" + value + "</option>")
    )
}

function getSelectedColor() {
    let colorSelector = $("#colorSelector");
    return colorSelector.val();
}

function getSelectedSize() {
    let sizeSelector = $("#sizeSelector");
    return sizeSelector.val();
}

function AddToCart() {
    let units = $("#product-quantity-input").val();
    if (units === '0') {
        return;
    }

    function showSuccessMessage() {
        let toast = '<div class="toast toast-success">Se agregaron ' + units + ' ' + title + ' al carrito de compras</div>';
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

    if (getSelectedColor() == null || getSelectedSize() == null) {
        showErrorMessage("Debe seleccionar una talla y un color para el producto");
        return;
    }

    $.ajax({
        type: "POST",
        url: "/add_to_cart",
        // set content type header to use Flask response.get_json()
        contentType: "application/json",
        // convert data/object to JSON to send
        data: JSON.stringify({
            id: idValue,
            color: getSelectedColor(),
            size: getSelectedSize(),
            units: units,
            totalPrice,
            title,
            image: image_name
        }),
        success: function (data, status, xhttp) {
            showSuccessMessage();
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            showErrorMessage(XMLHttpRequest.responseText);
        }
    });
}