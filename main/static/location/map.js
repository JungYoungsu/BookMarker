locate = 0;
target = 0;

shelf = "";
seat = 0;
seatgroup = 0;


function showshelf(id){
	$('#shelf_'+id).show();
}

function hideshelf(){
	$('.shelf').hide();
}

function appendshape(top, left, id, i) {
	shape = $("<span id='shape_" + id + "' class='shape' style='top:" + top[i] + "px; left: " + left[i] + "px;'></span>");
	shape.appendTo('#shapes');
	if (top.length != i) {
		shape.animate({
				top: top[i+1],
				left: left[i+1],
		}, 1000);
	}
}

function setlocation(str) {
	$.ajax({
		type:"POST",
		url:"/location/setlocation/",
		data: {
			'location': str
		},
		dataType:"JSON",
		success: function(data) {
			console.log(data['location']);
			locate = data['location'];
			
			$("#man").css({
				top: data['top']-18,
				left: data['left']
			});
			setman();
			if(seat != 0) setseat(seat);
			path(locate, target);
		}
	})
}
function setman() {
	if(locate == 0) return;
	$("#man").show();
	src = $("#man").attr('src');
	setTimeout(function() {
		$("#man").attr('src', src);
	}, 0);
}
function clear() {
	target = 0;
	shelf = "";
	seat = 0;
	seatgroup = 0;
	clearInterval(rid);
	clearInterval(aid);
	$(".shape").remove();
	$('.shelf').hide();
}

function setseat(id){
	seat = id;
	$.ajax({
		type:"POST",
		url:"/location/setseat/",
		data: {
			'seat': seat,
			'location': locate
		},
		datatype:'JSON',
		success: function(data) {
			target = data['target'];
			seatgroup = data['seatgroup'];
			path(locate, target);
			
			$("#seat").css({
				top: data['top'],
				left: data['left']
			}).show();
			
			setman();
		}
	})
	console.log(seat);
}
function setshelf(id){
	shelf = id;
	$.ajax({
		type:"POST",
		url:"/location/setshelf/",
		data: {
			'shelf': shelf
		},
		datatype:'JSON',
		success: function(data) {
			target = data['target'];
			path(locate, target);
			setman();
		}
	})
	console.log(shelf);
}

rid = null;	// interval ID to remove shape
aid = null; // interval ID to append shape

function path(start, end){
	if(start == 0 || end == 0) return;
	$.ajax({
		type:"POST",
		url:"/location/path/",
		data: {
			'start' : start,
			'end' : end,
		},
		dataType:"JSON",
		success: function(data) {
			console.log(data['path']);
			clearInterval(rid);
			clearInterval(aid);
			$(".shape").remove();
			
			data['path'].forEach(function (p , i) {
				appendshape(data['top'], data['left'], p, i);
			});
			rid = setInterval( function() {
				data['path'].forEach(function (p , i) {
					$("#shape_"+p).remove();
				});
			},900);
			aid = setInterval( function() {
				data['path'].forEach(function (p , i) {
					appendshape(data['top'], data['left'], p, i);
				});
			},900);
		}
	});
}