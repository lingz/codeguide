// JavaScript Document

// Initial Variables
$(window).load(function(){
barExists = 0;
lockedLanguage = "";
active = 0; //is an animation running?
fadetime = 800; // how long should fade-in take?
state = 0;// 0=home, 1=searchResults, 2=@, 3=? 4=login
open = [];
faded = 0.8; // how greyed out interface buttons get when inactive
overlay = 0; // whether the overlay is active
external = 1; //whether external functions are searched
version = "3.2"; // which version of the language is being searched
version_expanded = 0; //whether the version selector is expanded
version_list=["2.6", "2.7", "3.0", "3.1", "3.2", "3.3", "3.4"]; //list of verison for current language

$(".link").hover(function(){
	if (lockedLanguage != $(this).attr('id') && active==1){
    $(this).animate({opacity:1}, 150);
	}},
function(){
	if (lockedLanguage != $(this).attr('id') && active==1){
	$(this).animate({opacity:faded}, 150);
	};
	});

$('#searchContainer').submit(searchStart);

});



function startup(){
	$('.languages').css("opacity","1");
	$('.buttons').css("opacity","1");
	window.scrollTo(0, 0);
	
	
	identifiers = ['#codeguide', '#python, #house', '#java, #at_sign', '#html, #question_mark', '#css, #login'];
	lagtime = 600;
	modifier = 100;
	for (var i=0; i<identifiers.length; i++) {
		
		if (i == 0) {
			$(identifiers[i]).animate({opacity: 1}, {duration: 400, queue: true});
		}
		else{
			$(identifiers[i]).delay(lagtime).animate({opacity: 1}, {duration: fadetime-modifier, queue: true});
			lagtime += modifier;
		}
	}
	setTimeout(function(){
		$('#house, #login, #at_sign, #question_mark, #python, #java, #html, #css').animate({opacity: 0.8}, 400);
		active = 1;}, lagtime);
};



function changeLock(language) {
	
	if (active==1) {
		lockedLanguage = language;
		active = 0;
		locked = [];
		
	if (barExists == 0) {
		createSearch();
	}
	if (version_expanded = 1){
		collapse_version_list();
	}
	if (state == 1) {
		searchStart();
		setTimeout(function(){changeColor(language);}, 200);
	}
	else{
		changeColor(language);
	}
	active = 1;
	



}}

function returnColor(color){
	if (color=='python') {
		return "#00A0B0";
	}

	if (color=='java'){
		return "#CC333F";
	}

	if (color=='html'){
		return "#EB6841";
	}

	if (color=='css'){
		return "#EDC951";
	}
}

function changeColor(language){
	var newCol = returnColor(language);
	languageList = ["python", "java", "html", "css"];
	for (var i = 0; i<languageList.length; i++) {
		if (languageList[i] == language){
			//$(languageList[i]).attr('class', "link locked");
			$("#" +languageList[i]).animate({opacity:1}, 300);
		}
		else {
			//$(languageList[i]).attr('class', "link unlocked");
			$("#" +languageList[i]).animate({opacity:0.6}, 300);
		}
		$("#house, #at_sign, #question_mark, #login").animate({opacity:0.6}, 300);
		faded=0.6;
	}
	$("#divider2, #searchButton, #resultDivider, ul li span, #external_select").animate({
	       backgroundColor: newCol
	    }, { duration: 200, queue: false });
//	$("#searchButton").animate({
//	       backgroundColor: newCol
//	    }, { duration: 200, queue: false });
//	$("#resultDivider").animate({
//	       backgroundColor: newCol
//	    }, { duration: 200, queue: false });
	if (barExists == 0) { 
		$('#activeSearch').fadeIn(700);
		barExists = 1;
	}
	$('#results').attr({class: lockedLanguage});
	active = 1;
	}

function createSearch(){
	var searchBar = document.createElement("input");
	searchBar.type = "text";
	searchBar.id = "searchBar";
	searchBar.placeholder = "Search for...";
	var searchButton = document.createElement("input");
	searchButton.id = "searchButton";
	searchButton.type = "button";
	searchButton.value = "Guide Me!";
	searchButton.onclick = "searchStart();"
	var divider = document.createElement("div");
	divider.id = "divider";
	var divider2 = document.createElement("div");
	divider2.id = "divider2";
	var searchContainer = $("#searchContainer");
	searchContainer.css({"position": "relative"});
	searchContainer.append(searchBar);
	searchContainer.append(searchButton);
	searchContainer.append(divider);
	searchContainer.append(divider2);
}

function lift(){
	if (state == 0){
		active = 0;
	$('.search').animate({top: '10px'}), 450;
	$('#home.navbar').animate({top: "0%", marginTop: "0px"}, {duration:450, queue: false});
	$('.languages').animate({height: '0px', opacity: '0'}, {duration:450, queue: false});
	$('#resultDivider').css({"-moz-border-radius":"30px",
	"border-radius": "30px","margin-left": "auto","margin-right": "auto", "width": "700px", "height": "10px", "margin-top": "30px", "opacity": 0});
	setTimeout(function() {$("#external_select, #search_options").show(); $("#python").css({"marginTop":"18px"}); $('.languages').css({"width": '210px','height': '800px', 'position': 'absolute', 'right': '840px', 'top':'33px'});$('.languages').animate({'right': 820, 'opacity': 1}, 200);active = 1;}, 460);}
	$('#resultDivider').animate({opacity: '1'}, 450);
	$('#home').css({"background": "#eeeeee"});
	
}
function loginStart(loginType){
	$.ajax({
		url: 'http://i5.abudhabi.nyu.edu/~lz781/cgi-bin/loginInterface.py',
		type:  'post',
		datatype:  'html',
		data: {
			'loginType': loginType,
			'username': $("#login").val(),
			'password': $("#password").val()
		},
		success: function(response){
			$("#loginOutput").html(response);
		},
		error: function(jqXHR, textStatus, errorThrown){
	        // log the error to the console
	        console.log(
	            "The following error occured: "+
	            textStatus, errorThrown
	        );
	        }

	});
}
function searchStart(){
	$('#results').fadeOut(200, function(){window.scrollTo(0, 0);});
	input = $("#searchBar").val();
	$.ajax({
		url: 'http://i5.abudhabi.nyu.edu/~lz781/cgi-bin/codeguide_main.py',
		type:  'post',
		datatype:  'html',
		data: {
			'query': input,
			'language': lockedLanguage,
			'version': version,
			'expandable': external
		},
		success: function(response){
			genContent(response);
		},
		error: function(jqXHR, textStatus, errorThrown){
	        // log the error to the console
	        console.log(
	            "The following error occured: "+
	            textStatus, errorThrown
	        );
	        }

	});
	
	
	
	return false;
	
	};
	
function genContent(response){

	num_results = 4;
	var introQueue = $({});
	introQueue.queue("introQueue", function(next){lift(); state=1; next(); $("introQueue").dequeue;});
	introQueue.queue("introQueue", function(next) {
	setTimeout( function(){
	$('#results').css({"margin-top": "190px"});
//	$('#results').html("<div id='cr1'><div id='hr1'>header</div> <div id='rr1'>these are the results these are the results these are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the results </div> </div><div id='cr1'><div id='hr1'>header</div> <div id='rr1'>these are the results these are the results these are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the results </div> </div><div id='cr1'><div id='hr1'>header</div> <div id='rr1'>these are the results these are the results these are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the results </div> </div><div id='cr1'><div id='hr1'>header</div> <div id='rr1'>these are the results these are the results these are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the results </div> </div><div id='cr1'><div id='hr1'>header</div> <div id='rr1'>these are the results these are the results these are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the results </div> </div><div id='cr1'><div id='hr1'>header</div> <div id='rr1'>these are the results these are the results these are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the results </div> </div><div id='cr1'><div id='hr1'>header</div> <div id='rr1'>these are the results these are the results these are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the results </div> </div><div id='cr1'><div id='hr1'>header</div> <div id='rr1'>these are the results these are the results these are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the results </div> </div><div id='cr1'><div id='hr1'>header</div> <div id='rr1'>these are the results these are the results these are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the results </div> </div><div id='cr1'><div id='hr1'>header</div> <div id='rr1'>these are the results these are the results these are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the results </div> </div><div id='cr1'><div id='hr1'>header</div> <div id='rr1'>these are the results these are the results these are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the results </div> </div><div id='cr1'><div id='hr1'>header</div> <div id='rr1'>these are the results these are the results these are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the results </div> </div><div id='cr1'><div id='hr1'>header</div> <div id='rr1'>these are the results these are the results these are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the results </div> </div><div id='cr1'><div id='hr1'>header</div> <div id='rr1'>these are the results these are the results these are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the results </div> </div><div id='cr1'><div id='hr1'>header</div> <div id='rr1'>these are the results these are the results these are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the results </div> </div><div id='cr1'><div id='hr1'>header</div> <div id='rr1'>these are the results these are the results these are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the results </div> </div><div id='cr1'><div id='hr1'>header</div> <div id='rr1'>these are the results these are the results these are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the results </div> </div><div id='cr1'><div id='hr1'>header</div> <div id='rr1'>these are the results these are the results these are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the results </div> </div><div id='cr1'><div id='hr1'>header</div> <div id='rr1'>these are the results these are the results these are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the results </div> </div><div id='cr1'><div id='hr1'>header</div> <div id='rr1'>these are the results these are the results these are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the resultsthese are the results these are the results </div> </div>");
	$('#results').html(response);
	$('#results').fadeIn(200, function(){$(this).css({opacity: 1});});
	
	for (var i = 0; i<num_results; i++){
		$('#rc'+i).delay(50*(i+1)).animate({opacity: '1', marginTop: '10px'},200);
	}
	
	$("#results > div").hover(function(){
	    $(this).css({'background-color': hexToRGBA(returnColor(lockedLanguage),0.2)});
		},
	function(){
			if (open.indexOf($(this).attr("id")) == -1) {
		$(this).css({background: "none"});
			}
		});
	$("#results > div").click(function(){
		if  (open.indexOf($(this).attr("id")) == -1){
		$(this).css({'background-color': hexToRGBA(returnColor(lockedLanguage),0.2), 'overflow': "auto"});
		$(this).animate({'height':'200px'}, {duration:200, queue: false});
		$(this).children(":first").animate({'line-height':'200px'},{duration:200, queue: false});
		$(this).children().animate({'height':'200px'}, {duration:200, queue: false});
		open.push($(this).attr("id"));
		}
		else{
			$(this).css({'background-color': 'none', 'overflow': 'hidden'});
			$(this).children().animate({'height':'40px'}, {duration:200, queue: false});
			$(this).children(":first").animate({'line-height':'40px'},{duration:200, queue: false});
			$(this).animate({'height':'40px'}, {duration:200, queue: false});
			open.splice(open.indexOf($(this).attr("id")), 1);
		}
		
	});
	next();
	}, 500);
		}
	);
	introQueue.dequeue("introQueue");
	
}


function delContent(){
	$('#results').html("");
	
}

function hexToRGBA(hex, alpha){
	var r = parseInt(hex.substr(1,2),16).toString();
	var g = parseInt(hex.substr(3,2),16).toString();
	var b = parseInt(hex.substr(5,2),16).toString();
	
	return "rgba("+r+","+g+","+b+","+alpha+")";
}

    
function showOverlay(button){
	if (active==1){
	active = 0;
	$("#exit").hover(function(){
	    $("#exit").animate({opacity:1}, 150);
		},
	function(){
			$("#exit").animate({opacity:0.8}, 150);
		});
	$('#blackout, #prompt').show().animate({opacity:1}, {duration: 300, queue: false});
	$('#exit').show().animate({opacity:0.8}, {duration: 300, queue: false});
	if (button=="at_sign"){
		$('#prompt').html('<h1>Contact</h1><br><h3>Codeguide was originally developed by Lingliang Zhang of New York University Abu Dhabi. \
				<br><br>The project started in late 2012. Feel free to contact me for any reason at <a href="mailto:lz781@nyu.edu">lz781@nyu.edu</a>.</h3>');
	}
	if (button=="question_mark"){
		$('#prompt').html('<h1>What is Codeguide?</h1><br><h3>Codeguide is a multilingual programming language search engine designed \
				with programmers in mind. It was born out of frustration of having to constantly refer to sub-optimal interfaces to check for\
				function and method names. Codeguide is a work in progress, it will initially roll out with a search function in Python, Java, HTML and, \
				CSS. <br><br>In the future, it is hoped that it will support more languages and also popular libraries (i.e./ jQuery, pygame, etc). It is also hoped\
				that it will have a "translate" function, where the user types a function they know of from one module, Codeguide will find equivalent functions\
				from another specified language/library.</h3>');
	}
	if (button=="login"){
		$('#prompt').html('<h1>Login</h1><br><h3><form id=loginInterface" method="post"><input id="login" class="login" type="text" placeholder="username"><br>\
				<input id="password" class="login" type="password" placeholder="password"></form><div id="buttonContainer"><input id="loginButton" class="loginButton link" type="button" value="Login" onclick="loginStart(0)"> <input id="registerButton" class="loginButton link" type="button" value="Register" onclick="loginStart(1)"></div>\
				<div id="loginOutput"></div></h3>');
		$('#loginButton, #registerButton').hover(function(){
			    $(this).animate({opacity:1}, 150);
		},
			function(){
				$(this).animate({opacity:0.8}, 150);
				});
	}
	
	active = 1;
	}
}

function hideOverlay(){
	if (active==1){
	active = 0;
	$('#exit').off('mouseenter mouseleave').stop();
	$('#blackout, #prompt, #exit').delay(50).animate({opacity:0}, 300).delay(300).hide(0);
	active = 1;
	}
}

function version_select(element){
	if (active==1){
		active = 0;
		version_selected = element.id;		
		collapse_version_list();
		$("#version_selector").html("Version " +version_selected);
		active=1;
	}
}

function change_version(){
	if (active==1){
		active = 0;
		if (version_expanded == 0){
		if (lockedLanguage = "python"){
			rows = (version_list.length/3);
			if (version_list.length%3>0){
				rows = rows + 1;
			}
			$(".version_list").animate({"height":rows*20+1}, {queue: false});
			version_expanded = 1;
		}}
		else{
			collapse_version_list();
		}
		active = 1;
		}
		
	}

function collapse_version_list(){
	$(".version_list").animate({"height":0}, {queue: false});
	version_expanded = 0;
}

function toggle_external(){
	if (active==1){
		active = 0;
		if (external==1){
			external = 0;
			$("#external_select").animate({"opacity": 0.6}, 300);
		}
		else{
			external = 1;
			$("#external_select").animate({"opacity": 1}, 300);
		}
		active = 1;
	}
}