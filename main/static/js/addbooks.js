$(function() {
	$('#submit').click( function() {
		cid = $('#cid').val();
		
		$.ajax({
			type:"POST",
			url:"/book/getbook/",
			data: {'cid' : cid},
			dataType:"JSON",
			success: function(data) {
				$("#label").text(data['title'] + " - " + data['author'] + " : added");
			}
		});
	});
	
});

