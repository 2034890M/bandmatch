$(document).ready(function() {
	$('#player_search_form').hide()
	$('#band_search_form').hide();
	$('#player_button').click(function(){
		$('#player_search_form').show()
		$('#band_search_form').hide();
	});
	$('#band_button').click(function(){
		$('#band_search_form').show()
		$('#player_search_form').hide();
	});
});