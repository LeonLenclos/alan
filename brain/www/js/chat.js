
////////// VARS/////////////////

// state of the input
var input_open = false;
// id of the conversation
var conversation_id = null;

function setup_message_by_message_mode(argument) {

    //// ON SUBMINT ////
    function onSubmit(){
        if(!input_open) return;
        disableInput();
        talk($("#msg").val())
        $("#msg").val("");
    }

    $("#talk").on("click", onSubmit);
    $(window).keydown(function(event){
        // Event for pressing ENTER key
        if(event.keyCode == 13) {
            onSubmit();
            event.preventDefault();
            return false;
    }});

}

function setup_continuous_update_mode() {
    const DELAY = 100

    //// ON SUBMINT ////
    function onSubmit(){
        if(!input_open) return;
        disableInput();
        updateInput($("#msg").val(), true);
        $("#msg").val("");
    }

    $("#talk").on("click", onSubmit);
    $(window).keydown(function(event){
        // Event for pressing ENTER key
        if(event.keyCode == 13) {
            onSubmit();
            event.preventDefault();
            return false;
    }});

    //// ON INPUT ////
    $("#msg").on("input", function(e) {
        var input = $(this);
        var val = input.val();
        // update input if it has changed
        if (input.data("lastval") != val) {
            input.data("lastval", val);
            updateInput(val, false);
        }
    });

    //// AUTO UPDATE ////
    setInterval(getConv, DELAY);

}

////////// EVENTS //////////
$().ready(function(){

    // keys events
    $(window).keydown(function(event){
    	// Events for pressing Arrow key
    	if(event.keyCode == 38) { //UP
    		$("#discussion-container").animate({scrollTop : '-=50px'}, 200)
    		event.preventDefault();
    		return false;
    	}
    	if(event.keyCode == 40) { //DOWN
    		$("#discussion-container").animate({scrollTop : '+=50px'}, 200)
    		event.preventDefault();
    		return false;
    	}
    	// Give focus to the text input on keydown
    	if(!$("#msg").is(':focus')) {
        	$("#msg").focus();
        }
    });


});
///////// SET HTML FUNCTIONS //////////



// set status
function setStatus(msg) {
	$('#status').html(msg);
}

// disable the input and the button
function disableInput(){
	input_open = false;
	$("#talk").prop("disabled", true);
	$("#msg").prop("disabled", true);
}

// enable the input and the button
function enableInput(){
	input_open = true;
	$("#talk").prop("disabled", false);
	$("#msg").prop("disabled", false);
}

// update the discussion
function closeConversation() {
	// #discussion is a ul ellement (unordered list)
	setStatus('La conversation est fermée. Cliquez sur le [+] pour en ouvrir une nouvelle.')
	disableInput();
}

// update the discussion
function updateMessages(messages) {
	// #discussion is a ul ellement (unordered list)
	var discussion_html = '';

	if (messages) {
		$.each(messages, function(i,v){
			discussion_html += '<li class="'+v.speaker+'">'+v.msg+'</li>';
		});
	}

	if ($("#discussion").html() != discussion_html){
		$("#discussion").html(discussion_html);
		$("#discussion-container").scrollTop($('#discussion-container').prop("scrollHeight"));
	}
}


function appendMessage(message, speaker){
	var discussion_html = $("#discussion").html();
	discussion_html += '<li class="'+speaker+'">'+message+'</li>';
	$("#discussion").html(discussion_html);
	$("#discussion-container").scrollTop($('#discussion-container').prop("scrollHeight"));
}


//////////////// REQUEST ///////////////////

// catch errors
function catchError(jsonMsg) {
	// console.log(jsonMsg, jsonMsg.hasOwnProperty('err'))
	if(jsonMsg.hasOwnProperty('err')){
		setStatus(jsonMsg.err);
		disableInput();
		return true;
	} else {
		return false;
	}
}



//////////  OPEN CONVERSATIONS //////////


// Request a new conversation
function newConv() {
    conversation_id = null;
    disableInput();
    updateMessages();
    $.post("/new", '', newConvCallback, 'text');
    setStatus("Ouverture d'une nouvelle conversation.");
}

// Request the last conversation
function lastConv() {
    disableInput();
    updateMessages();
    $.post("/last", '', lastConvConvCallback, 'text');
    setStatus("Ouverture de la conversation.");

}

// Callback for new conversation request
function newConvCallback(response) {
    var jsonMsg = $.parseJSON(response);
    if(catchError(jsonMsg)) return;
    conversation_id = jsonMsg.conversation_id
    openConversation(jsonMsg.alan_status);
}
// Callback for last conversation request
function lastConvConvCallback(response) {
    var jsonMsg = $.parseJSON(response);
    if(catchError(jsonMsg)) return;
    conversation_id = -1;
    openConversation(jsonMsg.alan_status);
}

// Open a conversation
function openConversation(status) {
	setStatus("Conversation ouverte. ("+status+")");
	enableInput();

}




////////// UPDATE INPUT FUNCTION /////////

function updateInput(msg, finished) {

	// Empty string for msg
	if(msg === null) msg = "";

	// Create Json Msg (with user entry)
	var jsonMsg = {
		msg:msg,
		finished:finished,
		conversation_id:conversation_id
	};

	// Send POST request
    $.ajax({
        type: "POST",
        url: '/update_input',
        data: JSON.stringify(jsonMsg),
        contentType: "application/json; charset=utf-8",
        dataType: "text",
        success: updateInputCallback,
        failure: function(errMsg) {
            alert("Impossible d'envoyer le message à alan :'(");
        }
    });
  }

function updateInputCallback(response){
	jsonMsg = $.parseJSON(response);
	catchError(jsonMsg);
}


////////// TALK FUNCTION //////////
function talk(msg) {
    const RESPONSE_TIME_MIN = 4 * 1000;
    const RESPONSE_TIME_MAX = 6 * 1000;

	// prevent for talking to a closed conversation
	console.log('talk', msg)

	// Empty string for msg
	if(msg === null) msg = "";
	appendMessage(msg, 'human');

	// Create Json Msg (with user entry)
	var jsonMsg = {
		msg:msg,
		conversation_id:conversation_id
	};
    var start_time = Date.now();

	// Send POST request
    $.ajax({
        type: "POST",
        url: '/talk',
        data: JSON.stringify(jsonMsg),
        contentType: "application/json; charset=utf-8",
        dataType: "text",
        success: function(response) {
            var elapsed_time = Date.now() - start_time;
            var response_time = RESPONSE_TIME_MIN + (Math.random()*(RESPONSE_TIME_MAX-RESPONSE_TIME_MIN));
            if(elapsed_time<response_time){
                setTimeout(function() {
                    talkCallback(response);
                },response_time-elapsed_time);
            }
            else{
                talkCallback(response);
            }
        },
        failure: function(errMsg) {
            alert("Impossible d'envoyer le message à alan :'(");
        }
    });

}

function talkCallback(response){

	jsonMsg = $.parseJSON(response);
	if(catchError(jsonMsg)) return;
	appendMessage(jsonMsg.message, 'alan');
	enableInput();
	if(jsonMsg.close) closeConversation();
}


function secretTalk(msg) {

	// prevent for talking to a closed conversation
	if(!conversationOpen) return

	// Create Json Msg (with user entry)
	var jsonMsg = {
		msg:msg,
		conversation_id:conversation_id
	};

	// Send POST request
   	console.log("Sending msg : " +jsonMsg.msg)
    $.ajax({
        type: "POST",
        url: '/talk',
        data: JSON.stringify(jsonMsg),
        contentType: "application/json; charset=utf-8",
        dataType: "text",
        success: console.log,
        failure: console.log
    });
  }

////////// GET CONV //////////

function getConv() {

    if(conversation_id === null) return;

	// Create Json Msg (with user entry)
	var jsonMsg = {
		conversation_id:conversation_id
	};

	// Send POST request
    $.ajax({
        type: "POST",
        url: '/get_conv',
        data: JSON.stringify(jsonMsg),
        contentType: "application/json; charset=utf-8",
        dataType: "text",
        success: getConvCallback,
        failure: function(errMsg) {
		console.log('getConv failure')

            alert("Impossible de parler à Alan :'(");
        },
        timeout: 3000,
        error: function(jqXHR, textStatus, errorThrown) {
	        console.log('error ' + errorThrown)
	        // Empty conversation on errors.

	    }

    });

    // success callback
	function getConvCallback(response) {
		response = $.parseJSON(response)
		//catch errors in response
		if(catchError(response)){
			return;
		}
        if(response == undefined){
            updateMessages();
            disableInput();
            return;
        }
		updateMessages(response.messages || [])

        if(response.close) closeConversation();
		else if(response.messages){
			if(response.messages.length == 0){
				enableInput();
			} else {
				var last = response.messages[response.messages.length-1];
				if(last.speaker == 'alan'){
					if(last.finished){
						enableInput();
					}
					else {
						disableInput();
					}
				}
			}
		}
	}
}

