
	chrome.storage.sync.get("targetlist", function(res){
	if(window.location.href === res.targetlist)
	{
		chrome.storage.sync.set({targetshtml : document.querySelector('pre').innerHTML.replace(/ /g, "")},function(){
			window.close();
		})
	}
})
