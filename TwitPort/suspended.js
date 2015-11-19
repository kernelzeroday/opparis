

chrome.storage.sync.get('number', function(res1){
	chrome.storage.sync.get('targetshtml', function(res2){
		targets = res2.targetshtml.split("\n");
		chrome.storage.sync.set({'number':   parseInt(res1.number) + 1}, function(){
			
		window.location.assign("https://twitter.com/" + targets[parseInt(res1.number) + 2]+ "?number="+ (parseInt(res1.number) + 2) + "&tool=on")
	
		})
		})
})