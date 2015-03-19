$(document).ready( function() {
	$('#suggestion').keyup(function(){
        var query;
        query = $(this).val();
        $.get('/bandmatch/suggest_username/', {suggestion: query}, function(data){
         $('#user_list').html(data);
        });
	});
});