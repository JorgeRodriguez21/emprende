let product_detail_index = 0;

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
}