getRoi();
getTodaysMatches();
getPastMatches();

async function getTodaysMatches() {
	var model = document.getElementById("models").value;
	const matches = await fetch("website/"+ model +".csv");
	const data = await matches.text();
	const rows = data.split("\n");
	var dates = getDateList(true);
	var matchesFound = findMatches(rows, dates);
	var todayDiv = document.getElementById("tableToday")
	if (matchesFound.length != 0) {
		todayDiv.innerHTML = "";
		// creates table
		var table = todayDiv.appendChild(document.createElement("table"));
		// table header
		var thead = table.appendChild(document.createElement("thead"));
		var header = thead.appendChild(document.createElement("tr"));
		headerTitles = ["match", "bet", "p(bet)", "odd", "best bookmaker", "% of bankroll"];
		for (var i = 0; i < 6; i++) {
			header.appendChild(document.createElement("th")).textContent = headerTitles[i];
		}
		// table body
		var tbody = table.appendChild(document.createElement("tBody"));
		for (var i = 0; i<matchesFound.length; i++) {
			var vals = matchesFound[i].split(";");
			var match = vals[1] + " - " + vals[2];
			var bet = ["team1", "team2", "tie"];
			for (var k = 0; k < 3; k++) {
				var bankroll = (vals[16+k]*100).toFixed(2);
				if (bankroll<=0) {
					continue;
				}
				bankroll = bankroll + "%";
				var bet = bet[k];
				var pBet = (vals[4+k]*100).toFixed(2) + "%";
				var odd = vals[7+k];
				var bookmaker = vals[10+k];
				var rowContents = [match, bet, pBet, odd, bookmaker, bankroll];
				var row = tbody.appendChild(document.createElement("tr"));
				for (var j = 0; j < 6; j++) {
					var td = row.appendChild(document.createElement("td")).textContent = rowContents[j];
				}
			}
		} 
	}
	if (matchesFound.length == 0 || typeof td == 'undefined') {
		todayDiv.innerHTML = "";
		todayDiv.appendChild(document.createElement("SPAN")).textContent = "No potentially profitable matches were found for today."
	}
}

async function getPastMatches() {
	var model = document.getElementById("models").value;
	const matches = await fetch("website/"+ model +".csv");
	const data = await matches.text();
	const rows = data.split("\n");
	var dates = getDateList(false);
	var matchesFound = findMatches(rows, dates);
	var todayDiv = document.getElementById("tablePast")
	if (matchesFound.length != 0) {
		todayDiv.innerHTML = "";
		// creates table
		var table = todayDiv.appendChild(document.createElement("table"));
		// table header
		var thead = table.appendChild(document.createElement("thead"));
		var header = thead.appendChild(document.createElement("tr"));
		var headerTitles = ["match", "bet", "p(bet)", "odd", "best bookmaker", "% of bankroll"];
		for (var i = 0; i < 6; i++) {
			header.appendChild(document.createElement("th")).textContent = headerTitles[i];
		}
		// table body
		var tbody = table.appendChild(document.createElement("tBody"));
		for (var i = 0; i<matchesFound.length; i++) {
			var vals = matchesFound[i].split(";");
			var match = vals[1] + " - " + vals[2];
			var bet = ["team1", "team2", "tie"];
			for (var k = 0; k < 3; k++) {
				var bankroll = (vals[16+k]*100).toFixed(2);
				if (bankroll<=0) {
					continue;
				}
				 bankroll = bankroll + "%";
				var bet = bet[k];
				var pBet = (vals[4+k]*100).toFixed(2) + "%";
				var odd = vals[7+k];
				var bookmaker = vals[10+k];
				var rowContents = [match, bet, pBet, odd, bookmaker, bankroll];
				var outcome = vals[13+k];
				var row = tbody.appendChild(document.createElement("tr"));
				for (var j = 0; j < 6; j++) {
					if (j == 0) {
						var td = row.appendChild(document.createElement("td"));
						var span = td.appendChild(document.createElement("SPAN"));
						span.textContent = rowContents[j];
						if (outcome == 1) {
							span.classList.add("correct");
						} else {
							span.classList.add("wrong");
						}
					} else {
						var td = row.appendChild(document.createElement("td")).textContent = rowContents[j];
					}
				}
			}
		} 
	}
	if (matchesFound.length == 0 || typeof td == 'undefined') {
		todayDiv.innerHTML = "";
		todayDiv.appendChild(document.createElement("SPAN")).textContent = "No potentially profitable matches were found last week."
	}
}

function getDateList(today=true) {
	var date = new Date();
	var dateList = new Array();
	if (today) {
		dateList.push(("0" + date.getDate()).slice(-2) + '-' +("0" + (date.getMonth() + 1)).slice(-2) 
					   + '-' + date.getFullYear());
	} else {
		for (var i = 1; i <= 7 ; i++) {
			date.setDate(date.getDate() - 1);
			dateList.push(("0" + date.getDate()).slice(-2) + '-' +("0" + (date.getMonth() + 1)).slice(-2) 
							+ '-' + date.getFullYear());
		}
	}
	return dateList;
}

function findMatches(rows, dates) {
	// dates is an array
	var matchesFound = new Array();
	for (var i=0; i<rows.length; i++) {
		row = rows[i].split(';');
		if (dates.includes(row[0])) {
			matchesFound.push(rows[i]);
		}
	}
	return matchesFound;
}

async function getRoi() {
	const minMatches = 30;
	var model = document.getElementById("models").value;
	const matches = await fetch("website/"+ model +".csv");
	const data = await matches.text();
	const rows = data.split("\n");
	row = rows[0].split(';');
	if (row[25]>=minMatches) {
		var roi = ' ' + row[24] + ' (in ' + row[25] + ' bets)';
	} else {
		var roi = ' sample size too small';
	}
	var roiElement = document.getElementById("roi");
	roiElement.textContent = roi;
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