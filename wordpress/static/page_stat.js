
function text() {
	if (document.getElementById("text").style.display == "block"){
		document.getElementById("text").style.display = "none";
	}
	else{
		document.getElementById("text").style.display = "block";
	}
}

function word_count() {
	if (document.getElementById("word-count").style.display == "block"){
		document.getElementById("word-count").style.display = "none";
	}
	else{
		document.getElementById("word-count").style.display = "block";
	}
}

function word_bag(count) {
	var divs = document.getElementsByClassName("bar-words");
	for (var div=0; div<divs.length; div++){
		divs[div].style.display = "none";
	}
	document.getElementById(count).style.display = "block";
}