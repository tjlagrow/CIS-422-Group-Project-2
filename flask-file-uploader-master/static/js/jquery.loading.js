function loading(){
    $.ajax({
        type: "POST",
        url: "http://422hopper.pythonanywhere.com/",
        data: "n=1",
        beforeSend: function(){ 
            $('#mloader').show();
        },
        success: function(msg){
            //alert( msg );
        },
        error: function(xhr, option, error){
            alert(xhr.status);
            alert(error);
        },
        complete: function(){
            $('#mloader').hide();
        }
    });
}
