chrome.runtime.onMessage.addListener(function(message){
	
    
	if(message.number){
        chrome.browserAction.setBadgeText({text: "" + (parseInt(message.number)+1)})
    } else {
        var opt = {
        type: "basic",
        title: "TwitPort",
        message: "Done reporting the users on the list!",
        iconUrl: "unnamed.png"
    };
    try{
    chrome.notifications.create(opt).show();
    } catch(e) {
        
    }
    }
	
})

var Notification=(function(){
    var notification=null;
  
    return {
        display:function(opt){
            notification=chrome.notifications.create(opt);
            notification.show();
        },
        hide:function(){
            notification.close();
        }
    };
})();
  

 chrome.browserAction.onClicked.addListener(function(tab) {
    var action_url = "http://twitter.com/?start=true&tool=on";
    chrome.tabs.create({ url: action_url });
	chrome.storage.sync.get('targetlist', function(res){
		chrome.tabs.create({ url: res.targetlist });
	})
  });