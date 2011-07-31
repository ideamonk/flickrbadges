/* Author: 

*/
$(document).ready(function(){
    $("#flickrid").focus();
    
    $(".badge").hover(
        function(e){
            var badge = $(this).children("div");
            if (badge){
                badge.children("div.rule").stop().fadeIn();
            }
        },
        
        function(e){
            var badge = $(this).children("div");
            if (badge){
                badge.children("div.rule").stop().fadeOut();
            }
        }
    );
    
})






















