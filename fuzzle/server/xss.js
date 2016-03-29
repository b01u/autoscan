/*
 * author: b0lu
 * mail: b0lu@163.com
 */  
//创建webserver
var server = require('webserver').create();

//服务器监听端口
var host = '0.0.0.0:8654';

//返回的结果
var result = new Object();
result.isVul = false;

//判断是否为fuzzle msg 
var fuzzle_msg = "";

//检测是否有XSS漏洞
xssDetect = function(data,url,headers) {
	bpage.customHeaders = headers;
	bpage.setContent(data, decodeURIComponent(url));
	bpage.evaluate(function(){
		var tags = ["a", "abbr", "acronym", "address", "applet", "area", "article", "aside", "audio", "audioscope", "b", "base", "basefont", "bdi", "bdo", "bgsound", "big", "blackface", "blink", "blockquote", "body", "bq", "br", "button", "canvas", "caption", "center", "cite", "code", "col", "colgroup", "command", "comment", "datalist", "dd", "del", "details", "dfn", "dir", "div", "dl", "dt", "em", "embed", "fieldset", "figcaption", "figure", "fn", "font", "footer", "form", "frame", "frameset", "h1", "h2", "h3", "h4", "h5", "h6", "head", "header", "hgroup", "hr", "html", "i", "iframe", "ilayer", "img", "input", "ins", "isindex", "kbd", "keygen", "label", "layer", "legend", "li", "limittext", "link", "listing", "map", "mark", "marquee", "menu", "meta", "meter", "multicol", "nav", "nobr", "noembed", "noframes", "noscript", "nosmartquotes", "object", "ol", "optgroup", "option", "output", "p", "param", "plaintext", "pre", "progress", "q", "rp", "rt", "ruby", "s", "samp", "script", "section", "select", "server", "shadow", "sidebar", "small", "source", "spacer", "span", "strike", "strong", "style", "sub", "sup", "table", "tbody", "td", "textarea", "tfoot", "th", "thead", "time", "title", "tr", "tt", "u", "ul", "var", "video", "wbr", "xml", "xmp"];
		var eventHandler = ["mousemove","mouseout","mouseover", "click"];
		tags.forEach(function(tag) {
		        currentTags = document.querySelectorAll(tag);
		        if (currentTags !== null){
		            eventHandler.forEach(function(currentEvent){     
		                for(var i in currentTags){
		                    console.log(currentTags[i]);
		                    try {
		                        var ev = document.createEvent("MouseEvents");
		                        ev.initEvent(currentEvent, true, true);
		                        currentTags[i].dispatchEvent(ev);
		                    } catch (e) {
		                        continue;
		                    } 
		                }
		            });
		        }
		});
	});
};

//确认响应的msg是否为fuzzle的
isFuzzleMsg = function(msg){
	if(msg == fuzzle_msg){
		result.isVul = true;
	}
};

//初始化各种属性
initPage = function() {
	bpage = require("webpage").create();

	bpage.settings = {
		loadImages: true,
		localToRemoteUrlAccessEnabled: true,
		javascriptEnabled: true,
		webSecurityEnabled: false,
		XSSAuditingEnabled: false,
	};

	bpage.onAlert = function(msg) {
		isFuzzleMsg(msg);
	};
	
	bpage.onConsoleMessage = function(msg) {
		isFuzzleMsg(msg);
	};
	bpage.onConfirm = function(msg) {
		isFuzzleMsg(msg);
	};

	bpage.onPrompt = function(msg) {
		isFuzzleMsg(msg);
	};
	
	bpage.onError = function(msg) {
		isFuzzleMsg(msg);
	};
	
	return bpage;
};

//实例化一个page
var bpage = initPage();

//创建服务器
var service = server.listen(host , function(request, response) {
	console.log('Request at ' + new Date());
	
	if(request.method == "POST") {
		var durl = request.post["url"];
    	fuzzle_msg = request.post["fuzzle_msg"];
    	var dheaders = request.post["headers"];
    	var dresponse = request.post["response"];

		var headersDict = eval("["+dheaders+"]");

		xssDetect(dresponse,durl,headersDict);

		response.statusCode = 200;
		response.write(JSON.stringify(result));
		response.close();
		
	} else {
		response.statusCode = 500;
		response.write("Server is only designed to handle POST requests");
		response.close();
	}

	bpage.close()
	//全部重新初始化
	bpage = initPage();
	result.isVul = false;
	durl = null;
	dheaders = null;
	fuzzle_msg = null;
	dresponse = null;
	
});
if (service) {
    console.log('Web server running on host ' + host);
} else {
    console.log('Error: Could not create web server listening on host ' + host);
    phantom.exit();
}	
