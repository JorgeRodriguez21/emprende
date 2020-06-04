let product_detail_index = 0;


function setInitialIndexForOptions(numberOfExistentElements) {
    product_detail_index = parseInt(numberOfExistentElements) + 1;
}

function selectFile(id) {
    let files = document.getElementById("file_input").files;
    let file = files[0];
    if (!file) {
        return alert("No se ha seleccionado ningún archivo")
    }
    getSignedRequest(file, id);
}

function getSignedRequest(file, id) {
    let xhr = new XMLHttpRequest();
    let url = '';
    if (!id) {
        url = "/sign_s3?file_name=" + file.name + "&file_type=" + file.type + "&id=" + 0;
    } else {
        url = "/sign_s3?file_name=" + file.name + "&file_type=" + file.type + "&id=" + id;
    }
    xhr.open("GET", url);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                let response = JSON.parse(xhr.responseText);
                uploadFile(file, response.data, response.url);
            } else {
                alert("Could not get signed URL.");
            }
        }
    };
    xhr.send();
}

function uploadFile(file, s3Data, url) {
    let xhr = new XMLHttpRequest();
    xhr.open("POST", s3Data.url);

    let postData = new FormData();
    for (key in s3Data.fields) {
        postData.append(key, s3Data.fields[key]);
    }
    postData.append('file', file);

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200 || xhr.status === 204) {
                console.log('Esta es la url');
                console.log(url);
                document.getElementById("preview").src = url;
                document.getElementById("avatar-url").value = url;
            } else {
                alert("Could not upload file.");
            }
        }
    };
    xhr.send(postData);
}

function addProductOptions() {
    let rootContainer = $("#product-detail-container");
    const available_units_container = "<div id=\"options_container" + product_detail_index + "\" class=\"row\">\n" +
        "        <div id=\"available_units_container" + product_detail_index + "\" class=\"block\">\n" +
        "        <label for=\"available" + product_detail_index + "\">Unidades Disponibles:</label>\n" +
        "    <input type=\"number\" step=\"1\" pattern=\"\\d+\" min=\"0\" max=\"60000\" value=\"0\" id=\"available" + product_detail_index + "\"\n" +
        "    name=\"product_available\">\n" +
        "        </div>\n";
    const color_container = "<div id=\"color_container" + product_detail_index + "\" class=\"block\">\n" +
        "        <label for=\"color\">Color:</label>\n" +
        "    <input type=\"text\" id=\"color" + product_detail_index + "\" name=\"product_color\"/>\n" +
        "        </div>\n";
    const size_container = "<div id=\"size_container" + product_detail_index + "\" class=\"block\">\n" +
        "        <label for=\"size\">Talla:</label>\n" +
        "    <input type=\"text\" id=\"size" + product_detail_index + "\" name=\"product_size\"/>\n" +
        "        </div>\n" +
        "        </div>\n";
    rootContainer.append(available_units_container + color_container + size_container);
    product_detail_index++;
}

function getProductOptionsValues() {
    const productOptions = [];
    const containers = $('[id*="options_container"]');
    containers.toArray().forEach(container => {
            const units_container = $(container).children('[id*="available_units_container"]')[0];
            const units = $(units_container).children('input').val()
            const color_container = $(container).children('[id*="color_container"]')[0];
            const color = $(color_container).children('input').val()
            const sizeContainer = $(container).children('[id*="size_container"]')[0];
            const size = $(sizeContainer).children('input').val()
            productOptions.push({units: units, color: color, size: size});
        }
    )
    return JSON.stringify(productOptions);
}

function submitToServer() {
    let product_details_input = $("#product_details");
    product_details_input.val(getProductOptionsValues());
    const form = $('#product_form');
    const form_id = 'product_form';
    const url = form.prop('action');
    const type = form.prop('method');
    const formData = getProductFormData(form_id);

    // submit form via AJAX
    send_form(form, form_id, url, type, modular_ajax, formData);
}


function getProductFormData(form) {
    // creates a FormData object and adds chips text
    let formData = new FormData(document.getElementById(form));
    for (let [key, value] of formData.entries()) {
        console.log('formData', key, value);
    }
    return formData
}

function send_form(form, form_id, url, type, inner_ajax, formData) {
    // form validation and sending of form items
    if (!isFormDataEmpty(formData)) { // checks if form is empty
        event.preventDefault();
        // inner AJAX call
        inner_ajax(url, type, formData);
    } else {
        showErrorMessage("Todos los campos deben estar llenos antes de continuar");
    }
}

function isFormDataEmpty(formData) {
    let areEmptyFields = false;
    // checks for all values in formData object if they are empty
    for (const [key, value] of formData.entries()) {
        if (value === '' && value === []) {
            console.log("key", key)
            console.log("value", value)
            areEmptyFields = true;
        }
    }
    return areEmptyFields;
}

function modular_ajax(url, type, formData) {
    let toast_error_msg;
    let toast_category;
    // Most simple modular AJAX building block
    $.ajax({
        url: url,
        type: type,
        data: formData,
        processData: false,
        contentType: false,
        beforeSend: function () {
            // show the preloader (progress bar)

        },
        complete: function () {
            // hide the preloader (progress bar)

        },
        success: function (data) {
            showSuccessMessage();
        },
        error: function (xhr) {
            showErrorMessage();
        },
    }).done(function () {
        showSuccessMessage();
    });
};


function showSuccessMessage() {
    let toast = '<div class="toast toast-success">Producto almacenado correctamente</div>';
    $("body").append(toast);
    setTimeout(function () {
        $(".toast").addClass("toast-transition");
    }, 100);
    setTimeout(function () {
        $(".toast").remove();
        window.location.replace("/register_product")
    }, 3500);
}

function showErrorMessage(message) {
    let toast;
    if (message) {
        toast = "<div class=\"toast toast-error\">" + message + "</div>";
    } else {
        toast = '<div class="toast toast-error">Hubo un error al almacenar el producto</div>';
    }
    $("#product_form").append(toast);
    setTimeout(function () {
        $(".toast").addClass("toast-transition");
    }, 100);
    setTimeout(function () {
        $(".toast").remove();
    }, 3500);
    console.log(message);
}

function removeProductOptions() {
    let indexToRemove = product_detail_index - 1;
    if (indexToRemove < 0) {
        indexToRemove = 0;
    }
    console.log(indexToRemove)
    $("#options_container" + indexToRemove).remove();
    product_detail_index = indexToRemove;
}