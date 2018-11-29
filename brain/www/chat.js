$(document).ready(function(){

	// state of the conversation
	var conversation_open = false;
	// id of the conversation
	var conv = null;

	////////// GET A CONVERSATION ID //////////
	$.post('/new', '', newConvCallback,'text');
	function newConvCallback(response) {
		var response = $.parseJSON(response)
		//catch errors in response
		if(catchError(response)){
			return
		}
		// open conversation
		conv = response.conversation_id
		conversation_open = true
		console.log("Conversation open with id "+ conv)
		// write status
		$('#status').html("Conversation ouverte. ("+response.alan_status+")")
		// enable input
		enable_input()
	}


	////////// EVENTS //////////
	// Event for pressing ENTER key
	$(window).keydown(function(event){
		if(event.keyCode == 13) {
			talk()
  			event.preventDefault();
  			return false;
		}
	});
	// Event for pressing #talk button
	$("#talk").click(talk);


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
	function addToDiscussion(txt, speaker) {
		// #discussion is a ul ellement (unordered list)
		var new_entry = '<li class="'+speaker+'">'+txt+'</li>'
		var discussion = $("#discussion").html()
		$("#discussion").html(discussion + new_entry)
		// scroll to the bottom (with animation)
		$("#discussion-container").animate(
			{ scrollTop: $('#discussion-container').prop("scrollHeight")}, 1000);
	}

	//catch errors
	function catchError(jsonMsg) {
		if(jsonMsg.hasOwnProperty('err')){
			alert('/!\\ ERREUR /!\\\n' + jsonMsg.err + '\n\n(Essaye de recharger la page...)');
			return true;
		} else {
			return false;
		}

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
});
