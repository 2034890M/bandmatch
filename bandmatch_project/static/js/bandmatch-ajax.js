$(document).ready( function() {
	$('#suggestion').keyup(function(){
        var query;
        query = $(this).val();
        $.get('/bandmatch/suggest_username/', {suggestion: query}, function(data){
            $('#user_list').html(data);
        });
	});

	$('#suggest_mem').keyup(function(){
        var query;
        query = $(this).val();
        var slug;
        slug = $('#band_slug')[0].value
        $.get('/bandmatch/suggest_member/'+slug+'/', {suggest_mem: query}, function(data){
            $('#member_list').html(data);
        });
	});
    
    $('#suggest_band').keyup(function(){
        var query
        query = $(this).val();
        $.get('/bandmatch/suggest_band/', {suggest_band: query}, function(data){
            $('#your_bands_list').html(data);
        });
    });
});