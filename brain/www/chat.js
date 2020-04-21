$(document).ready(function(){

	////////// VARS/////////////////

	// state of the conversation
	var conversationOpen = false;
	// id of the conversation
	var conv = null;



	////////// EVENTS //////////
	// keys events
	$(window).keydown(function(event){
		// Event for pressing ENTER key
		if(event.keyCode == 13) {
			talk();
  			event.preventDefault();
  			return false;
		}
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
		// Events for secret talk
		if(event.keyCode == 112) { //F1
			secretTalk('f1')
  			return false;
		}
		if(event.keyCode == 113) { //F2
			secretTalk('f2')
  			return false;
		}
		if(event.keyCode == 114) { //F3
			secretTalk('f3')
  			return false;
		}
		if(event.keyCode == 115) { //F4
			secretTalk('f4')
  			return false;
		}
		if(event.keyCode == 119) { //F8
			secretTalk('f8')
  			return false;
		}
		// Give focus to the text input on keydown
		if(!$("#msg").is(':focus')) {
        	$("#msg").focus();
        }
	});

	// Event for typing
	$("#msg").on("input", function(e) {
		var input = $(this);
  		var val = input.val();
  		// update input if it has changed
  		if (input.data("lastval") != val) {
    		input.data("lastval", val);
	    	updateInput(val, false);
	  	}
	});

	// Event for pressing talk button
	$("#talk").on("click", talk);

	// Event for pressing new button
	$("#new").on("click", newConv);


	// Event for pressing open about
	$("#openAbout").on("click", function(e){
		$("#about").toggleClass('closed');
	});

	// Event for pressing close
	$(".close").on("click", function(e){
		var box = $(this).parent().parent();
		box.toggleClass('closed');
	});


	///////// SET HTML FUNCTIONS //////////


	
	// set status
	function setStatus(msg) {
		$('#status').html(msg);
	}

	// disable the input and the button
	function disableInput(){
		$("#talk").prop("disabled", true);
		$("#msg").prop("disabled", true);
	}

	// enable the input and the button
	function enableInput(){
		$("#talk").prop("disabled", false);
		$("#msg").prop("disabled", false);
	}

	// update the discussion
	function updateDiscussion(conv) {
		// #discussion is a ul ellement (unordered list)
		var discussion_html = '';

		var conversationOpen = !conv.close;

		if (conv.close) {
			setStatus('La conversation est fermée. Cliquez sur le [+] pour en ouvrir une nouvelle.')
		}

		if (conv.messages) {
			$.each(conv.messages, function(i,v){
				discussion_html += '<li class="'+v.speaker+'">'+v.msg+'</li>';
			});
		}


		if ($("#discussion").html() != discussion_html){
			$("#discussion").html(discussion_html);
			$("#discussion-container").scrollTop($('#discussion-container').prop("scrollHeight"));
		}

		if(!conv.messages
			||
			(conv.messages.length>0
			&& !conv.messages[conv.messages.length-1].finished
			&& conv.messages[conv.messages.length-1].speaker == 'alan')
			|| !conversationOpen ){
			disableInput();
		}
		else{
			enableInput();
		}
	}




	//////////////// REQUEST ///////////////////

	// catch errors
	function catchError(jsonMsg) {
		// console.log(jsonMsg, jsonMsg.hasOwnProperty('err'))
		if(jsonMsg.hasOwnProperty('err')){
			var newConvLink = $('<a>')
				.html('Nouvelle conversation')
				.addClass('buttonStyle')
				.on("click", newConv);
			$('#status').html(jsonMsg.err)
				.append(newConvLink);

			conversationOpen = false;
			disableInput();
			return true;
		} else {
			return false;
		}
	}



	//////////  OPEN CONVERSATIONS //////////
	

	// Request a new conversation
	function newConv() {
		requestConv("Ouverture d'une nouvelle conversation.", "/new");
	}
	
	// Request the last conversation
	function lastConv() {
		requestConv("Ouverture de la conversation.", "/last");
	}

	// Request a conversation
	function requestConv(statusMsg, methodURL){
		setStatus(statusMsg);
		disableInput();
		conversationOpen = false;
		updateDiscussion([]);
		$.post(methodURL, '', requestConvCallback, 'text');
	}

	// Callback for conversation request
	function requestConvCallback(response) {
		var jsonMsg = $.parseJSON(response);
		//catch errors in response
		if(catchError(jsonMsg)) return;
		// open conversation
		openConversation(jsonMsg.conversation_id, jsonMsg.alan_status);
	}

	// Open a conversation
	function openConversation(id, status) {
		if(GET_CONV_METHOD == 'last') {
			conv = -1;
		} else {
			conv = id;
		}
		conversationOpen = true;
		setStatus("Conversation ouverte. ("+status+")");
		enableInput();
	}




	////////// UPDATE INPUT FUNCTION /////////

	
	function talk() {
		updateInput($("#msg").val(), true);
		$("#msg").val("");
	}

	function updateInput(msg, finished) {

		// prevent for talking to a closed conversation
		if(!conversationOpen) return;

		// Empty string for msg
		if(msg === null) msg = "";

		// Create Json Msg (with user entry)
		var jsonMsg = {
			msg:msg,
			finished:finished,
			conversation_id:conv
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
	function secretTalk(msg) {

		// prevent for talking to a closed conversation
		if(!conversationOpen) return

		// Create Json Msg (with user entry)
		var jsonMsg = {
			msg:msg,
			conversation_id:conv
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
		if(GET_CONV_METHOD == 'last'){
			lastConv();
		}
		else if(!conversationOpen){
			return
		}
		// Create Json Msg (with user entry)
		var jsonMsg = {
			conversation_id:conv
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
				return
			}
			updateDiscussion(response)
		}

	}
				////////// GET STATUS //////////
		// function getStatus() {
		// 	if(GET_CONV_METHOD == 'last'){
		// 		lastConv();
		// 	}
		// 	else if(!conversationOpen){
		// 		return
		// 	}
		// 	// Create Json Msg (with user entry)
		// 	var jsonMsg = {
		// 		conversation_id:conv
		// 	};

		// 	// Send POST request
	 //        $.ajax({
	 //            type: "POST",
	 //            url: '/get_conv',
	 //            data: JSON.stringify(jsonMsg),
	 //            contentType: "application/json; charset=utf-8",
	 //            dataType: "text",
	 //            success: getConvCallback,
	 //            failure: function(errMsg) {
		// 			console.log('getConv failure')

	 //                alert("Impossible d'envoyer le message à alan :'(");
	 //            },
	 //            timeout: 3000,
	 //            error: function(jqXHR, textStatus, errorThrown) {
		// 	        console.log('error ' + errorThrown)
		// 	        // Empty conversation on errors.

		// 	    }

	 //        });

	 //        // success callback
		// 	function getConvCallback(response) {
		// 		response = $.parseJSON(response)
		// 		//catch errors in response
		// 		if(catchError(response)){
		// 			return
		// 		}
		// 		updateDiscussion(response)
		// 	}

		// }

		/////////////////// LETS GO /////////////////////////
		if(GET_CONV_METHOD == 'new'){
			newConv();
		}
		else if(GET_CONV_METHOD == 'last'){
			lastConv();
		}

		var timer, delay = 100;
		 setInterval(getConv, delay);
		 // setInterval(getStatus, 1000);
});
