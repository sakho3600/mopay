var $j = jQuery.noConflict();
window.setInterval(function(){
	$j("#msg").slideUp();
}, 10000);


function showLoading(){
    $j('#loading').fadeIn(100);
}

function hideLoading(){
    $j('#loading').fadeOut(100);
}

function showError(){
    $j('#nw-error-dialog').dialog('open');
    hideLoading();
}
