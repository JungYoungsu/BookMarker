$('#image').cropper({
  responsive: false,
  minContainerWidth:1000,
  minContainerHeight:700
});


$(function () {
	var console = window.console || { log: function () {} };
	var $image = $('#image');
	var $download = $('#download');
	var $dataX = $('#dataX');
	var $dataY = $('#dataY');
	var $dataHeight = $('#dataHeight');
	var $dataWidth = $('#dataWidth');
	var $dataRotate = $('#dataRotate');
	var $dataScaleX = $('#dataScaleX');
	var $dataScaleY = $('#dataScaleY');
	
	$('.docs-buttons').on('click', '[data-method]', function () {
		var $this = $(this);
		var data = $this.data();
		var $target;
		var result;

		if ($this.prop('disabled') || $this.hasClass('disabled')) {
		  return;
		}

		if ($image.data('cropper') && data.method) {
		  data = $.extend({}, data); // Clone a new one

		  if (typeof data.target !== 'undefined') {
			$target = $(data.target);

			if (typeof data.option === 'undefined') {
			  try {
				data.option = JSON.parse($target.val());
			  } catch (e) {
				console.log(e.message);
			  }
			}
		  }

		  result = $image.cropper(data.method, data.option, data.secondOption);

		  switch (data.method) {
			case 'scaleX':
			case 'scaleY':
			  $(this).data('option', -data.option);
			  break;

			case 'getCroppedCanvas':
			  if (result) {

				// Bootstrap's Modal
				//$('#getCroppedCanvasModal').modal().find('.modal-body').html(result);

				if (!$download.hasClass('disabled')) {
				  $download.attr('href', result.toDataURL('image/jpeg'));
				}
				
				$.ajax({
					type:"POST",
					url:"/book/addsideimg/",
					data: {
						'img' : result.toDataURL('image/jpeg'),
						'cid' : $("#addbooklist option:selected").val()
					},
					dataType:"JSON",
					success: function(data) {
						if( ! data['success']) {
							alert(data['reason']);
						}
					}
				});
			  }

			  break;
		  }

		  if ($.isPlainObject(result) && $target) {
			try {
			  $target.val(JSON.stringify(result));
			} catch (e) {
			  console.log(e.message);
			}
		  }

		}
	});
	
// Import image
	var $inputImage = $('#inputImage');
	var URL = window.URL || window.webkitURL;
	var blobURL;

	if (URL) {
	$inputImage.change(function () {
	  var files = this.files;
	  var file;

	  if (!$image.data('cropper')) {
		return;
	  }

	  if (files && files.length) {
		file = files[0];

		if (/^image\/\w+$/.test(file.type)) {
		  blobURL = URL.createObjectURL(file);
		  $image.one('built.cropper', function () {

			// Revoke when load complete
			URL.revokeObjectURL(blobURL);
		  }).cropper('reset').cropper('replace', blobURL);
		  $inputImage.val('');
		} else {
		  window.alert('Please choose an image file.');
		}
	  }
	  var img = new Image();
	  img.src = $image.attr("src");
	  img.onload = function() {
		$('#cropper').css("height", this.height+150);
		$('#hidescreen').css("height", this.height+250);
	  }
	});
	} else {
		$inputImage.prop('disabled', true).parent().addClass('disabled');
	}
});
