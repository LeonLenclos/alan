$(document).ready(function(){

	////////// VARS/////////////////
	// state of the conversation
	var conversation_open = false;
	// id of the conversation
	var conv = null;

	////////// CONVERSATIONS //////////
	function newConv() {
		$.post('/new', '', openConvCallback, 'text');
	}
	
	function lastConv() {
		$.post('/last', '', openConvCallback, 'text');
	}
	
	function openConvCallback(response) {
		var response = $.parseJSON(response)
		//catch errors in response
		if(catchError(response)){
			return
		}
		// open conversation
		openConversation(response.conversation_id, response.alan_status)
	}

	function openConversation(id, status) {
		conv = id
		if(GET_CONV_METHOD == 'last'){
			conv = -1
		}
		conversation_open = true
		// write status
		$('#status').html("Conversation ouverte. ("+status+")")
		// enable input
		enable_input()
	}

	////////// EVENTS //////////
	// keys events
	$(window).keydown(function(event){
		// Event for pressing ENTER key
		if(event.keyCode == 13) {
			update_input($("#msg").val(), true);
			$("#msg").val("");
  			event.preventDefault();
  			return false;
		}
		// Event for pressing Arrow key
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

		if(!$("#msg").is(':focus')) {
        	$("#msg").focus();
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
		if ($("#discussion").html() != discussion_html){
			$("#discussion").html(discussion_html)
			$("#discussion-container").scrollTop($('#discussion-container').prop("scrollHeight"));

		}
		// scroll to the bottom (with animation)


		if(conv.length>0 && !conv[conv.length-1].finished && conv[conv.length-1].speaker == 'alan'){
			disable_input();
		}
		else{
			enable_input();
		}
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

		////////// GET CONV //////////
		function get_conv() {
			if(GET_CONV_METHOD == 'last'){
				lastConv();
			}
			else if(!conversation_open){
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
				console.log('get_conv failure')

	                alert("Impossible d'envoyer le message à alan :'(");
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
		function get_status() {
			if(GET_CONV_METHOD == 'last'){
				lastConv();
			}
			else if(!conversation_open){
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
				console.log('get_conv failure')

	                alert("Impossible d'envoyer le message à alan :'(");
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

		/////////////////// LETS GO /////////////////////////
		if(GET_CONV_METHOD == 'new'){
			newConv();
		}
		else if(GET_CONV_METHOD == 'last'){
			lastConv();
		}

		var timer, delay = 100;
		 setInterval(get_conv, delay);
		 setInterval(get_status, 1000);
});
