function uploadImage() {
    let img = document.getElementById('product_picture');
    const file = document.querySelector('input[type=file]').files[0];
    img.src = window.URL.createObjectURL(file);
}