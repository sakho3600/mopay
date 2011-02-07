function showDepartments(b){
    var id = "_" + b.id;
    showLoading();
    var _url = '/ajax/get_department_select?key='+b.value;
    $j.ajax({
        url: _url,
        type: "GET",
        success: function(data){
                    document.getElementById(id).innerHTML = '';
                    $j("#"+id).append(data);
                    hideLoading();
                },
        error: showError
    });
}
