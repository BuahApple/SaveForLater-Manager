//The main script to collect and download all tabs link instantly

port = null;

function dont(listab) {
	//console.log(listab)
	//var black = listab
	port = chrome.runtime.connectNative('com.buahapple.sfl.downloader');
	port.postMessage(listab);
};