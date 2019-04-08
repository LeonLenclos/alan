



$(document).ready(function(){

	////////// VARS/////////////////
	// state of the conversation
	var conversation_open = false;
	// id of the conversation
	var conv = null;

	////////// CONVERSATIONS //////////
	function newConv() {
		$.post('/new', '', openConvCallback,'text');
	}
	
	function lastConv() {
		$.post('/last', '', openConvCallback,'text');
	}
	
	function openConvCallback(response) {
		var response = $.parseJSON(response)
		console.log(response)
		//catch errors in response
		if(catchError(response)){
			return
		}
		// open conversation
		openConversation(response.conversation_id, response.alan_status)
	}

	function openConversation(id, status) {
		conv = id
		conversation_open = true
		console.log("Conversation open with id "+ conv)
		// write status
		$('#status').html("Conversation ouverte. ("+status+")")
		// enable input
		enable_input()
	}

	////////// EVENTS //////////
	// Event for pressing ENTER key
	$(window).keydown(function(event){
		if(event.keyCode == 13) {
			update_input($("#msg").val(), true);
			$("#msg").val("");
  			event.preventDefault();
  			return false;
		}
	});
	// Event for typing
	$("#msg").on("input", function(e) {
		var input = $(this);
  		var val = input.val();
  		if (input.data("lastval") != val) {
    		input.data("lastval", val);
	    	update_input(val, false);
	  	}
	});

	// Event for pressing #talk button
		//NO NEED
		//$("#talk").click(talk);

	// Event for when the user quit
		// JE NE SAIS PAS QUOI FAIRE. CA NE MARCHE PAS :
		// $(window).unload(quit)

	///////// SET HTML FUNCTIONS //////////
	// disable the input and the button
	function disable_input (){
		$("#talk").prop( "disabled", true );
		$("#msg").prop( "disabled", true );
	}

	// enable the input and the button
	function enable_input (){
		$("#talk").prop( "disabled", false );
		$("#msg").prop( "disabled", false );
	}

	// add a txt to the discussion. speaker must be 'human' or 'alan'
	// DEPRECIATED !!!!!!!!!!!!!!!!!!!!!!!
	function addToDiscussion(txt, speaker) {
		// #discussion is a ul ellement (unordered list)
		var new_entry = '<li class="'+speaker+'">'+txt+'</li>'
		var discussion = $("#discussion").html()
		$("#discussion").html(discussion + new_entry)
		// scroll to the bottom (with animation)
		$("#discussion-container").scrollTop($('#discussion-container').prop("scrollHeight"));
	}

	// update the discussion
	function updateDiscussion(conv) {
		// #discussion is a ul ellement (unordered list)
		var discussion_html = ''

		$.each(conv, function(i,v){
			discussion_html += '<li class="'+v.speaker+'">'+v.msg+'</li>'
		});
		var old_discussion = $("#discussion").html()
		$("#discussion").html(discussion_html)
		// scroll to the bottom (with animation)


		if(!conv[conv.length-1].finished && conv[conv.length-1].speaker == 'alan'){
			disable_input();
		}
		else{
			enable_input();
		}
		$("#discussion-container").scrollTop($('#discussion-container').prop("scrollHeight"));
	}

	//catch errors
	function catchError(jsonMsg) {
		if(jsonMsg.hasOwnProperty('err')){
			$('#status').html(jsonMsg.err + ' <a href="/">Nouvelle conversation</a>')

			return true;
		} else {
			return false;
		}

	}

	////////// QUIT FUNCTION //////////
	// ATTENTION : Cette fonction est pour plus tard et n'est appellée nulle part !
	// DEPRECIATED !!!!!!!!!!!!!!!!!!!!!!!
	function quit() {
		// prevent for quiting a closed conversation
		if(!conversation_open) return
		alert("test")
		// Create Json Msg (with quit query)
		var jsonMsg = {
			msg:"quit",
			conversation_id:conv
		};

		// Send POST request
       	console.log("Sending msg : " +jsonMsg.msg)
        $.ajax({
            type: "POST",
            url: '/talk',
            data: JSON.stringify(jsonMsg),
            contentType: "application/json; charset=utf-8",
            dataType: "text"
            });

	}

	////////// UPDATE INPUT FUNCTION /////////
	function update_input(msg, finished) {

		// prevent for talking to a closed conversation
		if(!conversation_open) return

		// Create Json Msg (with user entry)
		var jsonMsg = {
			msg:msg,
			finished:finished,
			conversation_id:conv
		};

		// Send POST request
       	console.log("Sending msg : " +jsonMsg.msg)
        $.ajax({
            type: "POST",
            url: '/update_input',
            data: JSON.stringify(jsonMsg),
            contentType: "application/json; charset=utf-8",
            dataType: "text",
            success: console.log,
            failure: function(errMsg) {
                alert("Impossible d'envoyer le message à alan :'(");
            }
        });
      }

	////////// TALK FUNCTION //////////
	function talk() {
		// prevent for talking to a closed conversation
		if(!conversation_open) return

		// Create Json Msg (with user entry)
		var jsonMsg = {
			msg:$("#msg").val(),
			conversation_id:conv
		};

	    // Add user entry to #discussion
	    addToDiscussion($("#msg").val(), "human")

		// clear and disable input waiting for the response
		$("#msg").val("");
		disable_input()

		// Send POST request
       	console.log("Sending msg : " +jsonMsg.msg)
        $.ajax({
            type: "POST",
            url: '/talk',
            data: JSON.stringify(jsonMsg),
            contentType: "application/json; charset=utf-8",
            dataType: "text",
            success: talkCallback,
            failure: function(errMsg) {
                alert("Impossible d'envoyer le message à alan :'(");
            }
        });

        // success callback
		function talkCallback(response) {
			response = $.parseJSON(response)
			//catch errors in response
			if(catchError(response)){
				return
			}
			// Add response to #discussion
       		console.log("Receiving msg : " +response.text)

			addToDiscussion(response.text, "alan")
			if(response.command != "quit"){
				// reenable input
				enable_input();
			} else {
				// if the quit command have been passed, close the conversation
				conversation_open = false;
				$('#status').html('Conversation fermée. <a href="/">Nouvelle conversation</a>')
			}
		}
	}

		////////// GET CONV //////////
		function get_conv() {
			if(GET_CONV_METHOD == 'last'){
				lastConv();
			}
			if(!conversation_open) return

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
	                alert("Impossible d'envoyer le message à alan :'(");
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

		/////////////////// LETS GO /////////////////////////
		if(GET_CONV_METHOD == 'new'){
			newConv();
		}
		else if(GET_CONV_METHOD == 'last'){
			lastConv();
		}

		var timer, delay = 100;
		timer = setInterval(get_conv, delay);

});
