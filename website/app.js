getTodayMatches();

async function getTodayMatches() {
	const matches = await fetch("website/data.csv");
	const data = await matches.text();
	console.log(data);
}

function readMore() {
	var dots = document.getElementById("dots");
	var moreText = document.getElementById("more");
	var readMore = document.getElementById("readMore");

	if (dots.style.display === "none") {
		dots.style.display = "inline";
		readMore.innerHTML = "Read more"; 
		moreText.style.display = "none";
	} else {
		dots.style.display = "none";
		readMore.innerHTML = "Read less"; 
		moreText.style.display = "inline";
	}
}