function stf_click(){
    $j('#product_description').hide();
    $j('#p_stf').fadeIn(1000);

    $j('#stf-btn').hide();
    $j('#show-des-btn').fadeIn(1000);
}

function show_description_click(){
    $j('#p_stf').hide();
    $j('#product_description').fadeIn(1000);

    $j('#show-des-btn').hide();
    $j('#stf-btn').fadeIn(1000);
}
