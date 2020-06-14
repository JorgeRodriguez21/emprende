let maxValue = undefined;
let idValue = undefined;
let totalPrice = undefined;
let title = undefined;
let image_name = undefined
let options_array = undefined
let available_units = undefined

function getColorsArray(options_array) {
    let colors = options_array.map(option => {
        return option.color
    });
    colors = colors.slice().sort((first, second) => {
        return first > second;
    }).reduce(function (first, second) {
        if (first.slice(-1)[0] !== second) first.push(second);
        return first;
    }, []);
    return colors;
}

function OpenProduct(id, image_name_param) {
    const options = $('.add_to_cart input[name=articleid]').val();
    options_array = JSON.parse(JSON.parse(options));
    let colors = getColorsArray(options_array);
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

    $(".lightbox-blanket").toggle();

    createColorSelector(colors);
    createSizesSelector(undefined);

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
    let value = $("#product-quantity-input").val();
    CalcPrice(value);
});

function createColorSelector(values) {
    let colorSelector = $("#colorSelector");
    colorSelector.html("");
    if (values.length > 0) {
        colorSelector.append("<option selected disabled hidden>Seleccione un color ...</option>");
    }

    values.forEach(value =>
        colorSelector.append("<option value=\"" + value + "\">" + value + "</option>")
    )
}

function createSizesSelector(selectedColor) {
    const sizesAvailableForSelectedColor = options_array.map(option => {
        if (selectedColor === option.color && option.available_units > 0) {
            return option.size
        }
    }).filter(size => !!size);
    let sizeSelector = $("#sizeSelector");

    sizeSelector.html("");
    if (sizesAvailableForSelectedColor.length > 0) {
        sizeSelector.append("<option selected disabled hidden>Seleccione la talla ...</option>");
        sizesAvailableForSelectedColor.forEach(value =>
            sizeSelector.append("<option value=\"" + value + "\">" + value + "</option>"))
    } else {
        sizeSelector.append("<option selected disabled hidden>Seleccione otro color</option>");
    }

    updateAvailableUnits();
}

function getSelectedColor() {
    let colorSelector = $("#colorSelector");
    return colorSelector.val();
}

function updateSizesColor() {
    createSizesSelector(getSelectedColor());
}

function getSelectedSize() {
    let sizeSelector = $("#sizeSelector");
    return sizeSelector.val();
}

function updateAvailableUnits() {
    if (!getSelectedColor() || !getSelectedSize()) {
        available_units = 0;
        maxValue = parseInt(available_units);
        let dialogAvailableUnits = $('.lightbox-blanket .product-available');
        $(dialogAvailableUnits).html('Debe seleccionar color y talla para saber el n&uacute;mero de unidades disponibles');
    } else {
        let available_units = options_array.find(option => {
            if (option.color === getSelectedColor() && option.size === getSelectedSize()) {
                return option;
            }
        }).available_units;
        maxValue = parseInt(available_units);
        let dialogAvailableUnits = $('.lightbox-blanket .product-available');
        $(dialogAvailableUnits).html("<b>" + available_units + "</b> Unidades disponibles");
    }
}

function AddToCart() {
    let units = $("#product-quantity-input").val();
    if (units === '0') {
        showErrorMessage("No puede agregar 0 unidades al carrito");
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

    if (!getSelectedColor() || !getSelectedSize()) {
        showErrorMessage("Debe seleccionar una talla y un color para el producto");
        return;
    }

    console.log(options_array);
    console.log(getOptionSelectedId());

    $.ajax({
        type: "POST",
        url: "/add_to_cart",
        // set content type header to use Flask response.get_json()
        contentType: "application/json",
        // convert data/object to JSON to send
        data: JSON.stringify({
            id: idValue,
            option_selected: getOptionSelectedId(),
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

function getOptionSelectedId() {
    return options_array.find(option => {
        if (option.size === getSelectedSize() && option.color === getSelectedColor()) {
            return option
        }
    }).id
}


//https://stackoverflow.com/questions/19728666/drop-down-box-dependent-on-the-option-selected-in-another-drop-down-box