(function(){

function setURL(){
	chrome.storage.sync.set({targetlist: document.querySelector('input').value},function(){
		document.body.innerHTML += "Url: " + document.querySelector('input').value + " has been saved! Now click on the add-on icon and \"shoot the canon\""
	});
}
 document.querySelector('button').onclick = setURL
chrome.storage.sync.get('targetlist',function(res){
		document.querySelector('input').value = res.targetlist
	});
})();