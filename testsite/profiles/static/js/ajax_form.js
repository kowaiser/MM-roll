function setupAjaxForm(form_id){
    var form = '#' + form_id;
    var form_message = form + '-message';

    var disableAll = function(val){
	var f = document.getElementById(form_id);
	var inputs = f.getElementsByTagName("input");
	for(var i = 0; i < inputs.length; i++){
		inputs[i].readOnly = val;
	};
	var inputs = f.getElementsByTagName("textarea");
	for(var i = 0; i < inputs.length; i++){
		inputs[i].readOnly = val;
	};
    };

    $(form).ajaxSend(function(){
        $(form_message).removeClass().addClass('loading').html('Uploading...').fadeIn();
    });

    var options = {
        dataType:  'json',
        beforeSubmit: function(){
            disableAll(true);
        },
        success: function(json){
            $(form_message).hide();
            $(form_message).removeClass().addClass(json.type).html(json.message).fadeIn('slow');
            disableAll(false);
        }
    };
    $(form).ajaxForm(options);
}

$(document).ready(function() {
    new setupAjaxForm('edit-profile');
});
