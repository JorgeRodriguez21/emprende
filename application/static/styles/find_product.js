function filterByName() {
    let input, filter, table, tr, td, i;
    input = document.getElementById("inputName");
    filter = input.value.toUpperCase();
    table = document.getElementById("content-table");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[0];
        if (td) {
            if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

// '.tbl-content' consumed little space for vertical scrollbar, scrollbar width depend on browser/os/platfrom. Here calculate the scollbar width .
$(window).on("load resize ", function () {
    const scrollWidth = $('.tbl-content').width() - $('.tbl-content table').width();
    $('.tbl-header').css({'padding-right': scrollWidth});
}).resize();


function goToOrderDetail(id) {
    document.location.href = '/order/' + id
}

function DoNav(id) {
    document.location.href = '/product/' + id
}