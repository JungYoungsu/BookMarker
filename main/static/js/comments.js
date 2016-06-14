$(document).ready(function() {

});

$(function() {
	$('#submit').click( function() {
		content = $('#content').val();
		
		$.ajax({
			type:"POST",
			url:"/addcomment/",
			data: {'content' : content},
			dataType:"JSON",
			success: function(data) {
				location.reload();
			}
		});
	});
	
});