//when extension is clicked it will trigger getfile() and then collect the html links on browser then
//send and execute dont() in themain.js then it will send it to native app

function getfile() {
	chrome.tabs.query({currentWindow: true}, function(tabs) {
		var a = [];
		tabs.forEach(function(tab){
			a.push(tab.url);
		});
		chrome.runtime.getBackgroundPage(function () {
            dont(a)});
	})
 };
 
chrome.browserAction.onClicked.addListener(getfile);