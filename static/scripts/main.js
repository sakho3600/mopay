var list_page_number = 2;
function get_more_products(type, key){
    var _url = '/ajax/list_more_products?page='+list_page_number+'&type='+type+'&key='+key;
    showLoading();
    $j.ajax({
        url: _url,
        type: "GET",
        success: function(data){
            var __id = "ab_" + Math.floor(Math.random()*99999);
            var _d = "<div id='" + __id + "' style='display: none;'>" + data + "</div>";
            $j('#more_products').append(_d);
            $j(document.getElementById(__id)).fadeIn(300);
            list_page_number += 1;
            hideLoading();
            },
        error: showError
    })
}
