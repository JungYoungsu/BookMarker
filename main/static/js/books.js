

$(document).ready(function() {
	$('#cropper').hide();
	$('#hidescreen').hide();
	$('#dataTables-example').DataTable({
			responsive: true,
			"order": [[ 0, "desc" ]]
	});
		
});

$('#showModal').click(function() {
	if( $('input[name=cbox]:checked').length < 1 ) {	// checkbox check
		alert("Check books");
		return;
	}
	
	$("input[name=cbox]:checked").each(function() {	//	select option add
		var id = $(this).val();
		var title = $('#booktitle_'+id).val();
		$("#addbooklist").append("<option value='" + id +"'>" + id + " : " + title + "</option>");
	});

	$('#cropper').show();
	$('#hidescreen').show();
});

$('#closeModal').click(function() {
	$('#cropper').hide();
	$('#hidescreen').hide();
	$("#addbooklist option").each(function(){	// modal selectoption reset
		this.remove();
	});
});


$('#boxclear').click(function() {
	$("#addbooklist option").each(function(){	// modal selectoption reset
		this.remove();
	});
	$("input[name=cbox]").each(function() {	// checkbox reset
		$(this).attr("checked",false);
	});
});

$('.btn.btn-info').click(function() {
	window.open(this.value,'_blank');
});



