$('#suggestion').keyup(function(){
        var query;
        query = $(this).val();
        $.get('/bandmatch/suggest_category/', {suggestion: query}, function(data){
         $('#cats').html(data);
        });
});