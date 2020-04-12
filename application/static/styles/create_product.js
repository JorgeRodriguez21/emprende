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