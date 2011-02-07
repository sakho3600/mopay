var $j = jQuery.noConflict();

function showLoading(){
    $j('#loading').fadeIn(100);
}

function hideLoading(){
    $j('#loading').fadeOut(100);
}

$j(function(){
    // Dialog			
    $j('#nw-error-dialog').dialog({
	    autoOpen: false,
	    width: 500,
	    buttons: {
		    "Ok": function() { 
			    $j(this).dialog("close"); 
		    }
	    }
    });

    // Dialog Link
    $j('#dialog_link').click(function(){
	    $j('#nw-error-dialog').dialog('open');
	    return false;
    });

});

function showError(){
    $j('#nw-error-dialog').dialog('open');
    hideLoading();
}
