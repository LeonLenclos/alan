$().ready(function(){

    $(window).keydown(function(event){
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
    });

});