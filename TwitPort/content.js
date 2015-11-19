function f(val) {
	var reportIframe = document.getElementById("new-report-flow-frame");
	var iframeHTML = reportIframe.contentDocument;
	if(iframeHTML.querySelector("input[type='radio'][value='" + val + "']") === null)
	{
		setTimeout(function(){ f(val)}, 500)
	} else {
		f2(iframeHTML, val)
	}
	
	
}

function f2(iframeHTML, val) {
	iframeHTML.querySelector("input[type='radio'][value='" + val + "']").click()
	document.querySelector('.new-report-flow-next-button').click()
}
function report(callback) {
	document.querySelector('.user-dropdown').click()
	document.querySelector('li.report-text button[type="button"]').click()


	setTimeout(function () { 
		f('abuse') 
		setTimeout(function () { f('harassment') 
			setTimeout(function () { f('Someone_else')
				setTimeout(function () { f('violence') 
					setTimeout(callback, 1000)
				 }, 1000)
			 }, 1000)
		}, 1000)
	}, 2000)
	
	
	
}



function $_GET(){
	var queryDict = {}
location.search.substr(1).split("&").forEach(function(item) {queryDict[item.split("=")[0]] = item.split("=")[1]})
return queryDict
}

chrome.storage.sync.get('targetshtml', function (res) {
	var targets = res.targetshtml.split("\n")
		getP = $_GET()
		if(getP['start'] || parseInt(getP['number']) < targets.length){
		target_url = targets[parseInt(getP['number'])]
		if (targets.length !== 0 && ("https://twitter.com/" + target_url + '?number='+ getP['number'] +'&tool=on'  )=== window.location.href) {
			if(document.querySelector('html').innerHTML.indexOf('Sorry, that page doesn’t exist!') === -1){
			window.onload = function() {report(function () {
					chrome.storage.sync.set({'number': getP['number']}, function(){
						chrome.runtime.sendMessage({'number': getP['number']})
					window.location.assign("https://twitter.com/" + targets[parseInt(getP['number']) + 1] + '?number=' + (parseInt(getP['number']) + 1) + '&tool=on')
				
					})
			})
			}
			} else {
				chrome.storage.sync.set({'number': getP['number']}, function(){
						chrome.runtime.sendMessage({'number': getP['number']})
					window.location.assign("https://twitter.com/" + targets[parseInt(getP['number']) + 1] + '?number=' + (parseInt(getP['number']) + 1) + '&tool=on')
				
					})
			}
		} else if (targets.length !== 0) {
			if(getP['start'] === 'true'){
			window.location.assign("https://twitter.com/" + targets[0] + '?number=0&tool=on')
			} else {
			chrome.runtime.sendMessage({showNotification: "true"}, function(res){
				window.close()
			})
			}
				
		}
		
		} else {
			chrome.runtime.sendMessage({showNotification: "true"}, function(res){
				window.close()
			})
		}

})
