locate = 0;
target = 0;

shelf = "";
seat = 0;
seat_top = 0;
seat_left = 0;
seatgroup = 0;

aid = null; // interval ID to append shape
rid = null;	// interval ID to remove shape

for (i = 1; i < 9; i++) {
	pannellum.viewer('panorama_' + i , {
		"type": "equirectangular",
		"panorama":  "/media/map/panorama/" + i + ".jpg",
		"showFullscreenCtrl": false
	});
}
$(function() {
	$('.cam').click( function() {		
		$("#panorama_container_"+ $(this).attr('id').split("_")[1]).show();
	});
	$('.button').click( function() {
		$(".panorama_container").hide();
	});
});

function clear() {
	target = 0;
	shelf = "";
	seat = 0;
	seat_top = 0;
	seat_left = 0;
	seatgroup = 0;
	clearInterval(rid);
	clearInterval(aid);
	$(".shape").remove();
	$('#seat').hide();
}

function setlocation(str) {
	$.ajax({
		type:"POST",
		url:"/location/setlocation/",
		data: {
			'aplist': str
		},
		dataType:"JSON",
		success: function(data) {
			console.log(data['location']);
			locate = data['location'];
			if (data['top'] == 48) data['top'] = 58;
			
			$("#man").css({
				top: data['top']-20,
				left: data['left']-10
			});
			setman();
			if(seat != 0) setseat(seat); // 열람석 찾는 경우엔 setseat 시동(노트북열람석 - 보다 더 짧은 거리 찾기 위함)
			else path(locate, target);
		}
	})
}

function setman() { // to solve GIF animation error 
	if(locate == 0) return;
	$("#man").show();
	src = $("#man").attr('src');
	setTimeout(function() {
		$("#man").attr('src', src);
	}, 0);
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
			clear();
			seat = id;
			target = data['target'];
			seatgroup = data['seatgroup'];
			path(locate, target);
			
			$("#seat").css({
				top: data['top'],
				left: data['left']
			}).show();
			
			seat_top = data['top'];
			seat_left = data['left'];
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
			clear();
			shelf = id;
			target = data['target'];
			path(locate, target);
			
			setman();
		}
	})
	console.log(shelf);
}

function showshelf(id){ // id 어오는건 1_2 이런 식
	$('#shelf_'+id.split("_")[0]).show();
}

function hideshelf(){
	$('.shelf').hide();
}

function appendshape(top, left, id, i) { // 이동 경로용 빨간 동그라미
	shape = $("<span id='shape_" + id + "' class='shape' style='top:" + top[i] + "px; left: " + left[i] + "px;'></span>");
	shape.appendTo('#shapes');
	if (top.length != i) {
		shape.animate({
				top: top[i+1],
				left: left[i+1],
		}, 900);
	}
}

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
			
			if (seat != 0) {
				data['top'].push(seat_top + 17);
				data['left'].push(seat_left - 1);
				data['path'].push("seat");
			}
			
			
			data['path'].forEach(function (p , i) {
				appendshape(data['top'], data['left'], p, i);
			});
			rid = setInterval( function() {
				data['path'].forEach(function (p , i) {
					$("#shape_"+p).remove();
				});
			}, 900);
			aid = setInterval( function() {
				data['path'].forEach(function (p , i) {
					appendshape(data['top'], data['left'], p, i);
				});
			}, 900);
		}
	});
}