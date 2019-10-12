var el = x => document.getElementById(x);

function onLoadProc() {								// need to get rid of previously uploaded images
	el("file-input").value = null;
    el("button2").style.display = "none";		// hide "analyze" button until it's needed
}

function showPicker() {
	el("result-label").innerHTML = ``;			// erase previous image results
	el("file-input").click();
}

function showPicked(input) {						// image has been uploaded
	el("upload-label").innerHTML = input.files[0].name;		// currently  not used (not visible)
	var reader = new FileReader();
	reader.onload = function(e) {
		el("image-picked").src = e.target.result;
		el("image-picked").className = "";
		el("button2").style.display = "block";
		el("headerimg").classList.add("hide-for-small");
	};
	reader.readAsDataURL(input.files[0]);
}

function analyze() {									// get uploaded image and POST it to Flask "analyze" route
	var uploadFiles = el("file-input").files;
	if (uploadFiles.length !== 1) {					// test that there's a file already (shouldn't ever happen)
		alert ("Please upload a file to analyze.");
		return;
	}
	var image = new Image();							// test that it's actually an image file
	image.onload = function() {						// this means it's a real image file
		el("analyze-button").innerHTML = "Analyzing...";
		el("spinner1").classList.add("yes-display");
		el("spinner1").classList.remove("no-display");
		var xhr = new XMLHttpRequest();
		var loc = window.location;
		xhr.open("POST", `${loc.protocol}//${loc.hostname}:${loc.port}/analyze`, true);
		xhr.onload = function(e) {			// successful analysis
			if (this.readyState === 4) {
				var response = JSON.parse(e.target.responseText);
				el("result-label").innerHTML = `<div class="result">` + `${response["result"]}` + `</div>`;
			}
			el("spinner1").classList.add("no-display");
			el("spinner1").classList.remove("yes-display");
			el("analyze-button").innerHTML = "2. Analyze image";
		    el("button2").style.display = "none";		// hide "analyze" button again
		};
		xhr.onerror = function() {
			alert(xhr.responseText);
		};
		var fileData = new FormData();
		fileData.append("file", uploadFiles[0]);
		xhr.send(fileData);							// send the image for analysis
	};
	image.onerror = function() {					// not an image file (or not parseable)
		alert("Couldn't parse the file as an image.");
		return;
	};
	var URL = window.URL || window.webkitURL;
	image.src = URL.createObjectURL(uploadFiles[0]);		// make the test image
}
