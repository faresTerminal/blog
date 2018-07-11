$(document).ready( function(){
  $('.pl1 .list1 li h2').click(function(){
  $('.pl1 .list1 .child-list').fadeToggle();
  $('.pl1 .list1 .show').fadeToggle();

});
   $('.pl1 .list2 li h2').click(function(){
  $('.pl1 .list2 .child-list').fadeToggle();
  $('.pl1 .list2 .show').fadeToggle();


});

   $('.pl2 .list1 li h2').click(function(){
  $('.pl2 .list1 .child-list').fadeToggle();
  $('.pl2 .list1 .show').fadeToggle();

});
   $('.pl2 .list2 li h2').click(function(){
  $('.pl2 .list2 .child-list').fadeToggle();
  $('.pl2 .list2 .show').fadeToggle();

});

   $('#top').each(function(){
 $(this).click(function(){
  $('html, body').animate({ scrollTop: 0}, 2000);
  return false;
});   
});

   // add smokers

     $('.nav li a').click(function(){
        $('html, body').animate({
         scrollTop: $('#' + $(this).data('value')).offset().top

     }, 1000);
   });
  

  /* small bar */
$('#user h3').click(function(){
  $('#user_list').toggleClass('show');
  
    
});

                      /* prfile playing */
/* first edit*/
  $('.edit h6').click(function(){
   $('.edit .more_button1').fadeToggle();
   

});
 $('.edit .more_button1').click(function(){
   $('.edit .pass').fadeToggle();
   

});
 /* end edit div */
   $('.add_more h4').click(function(){
   $('.add_more .more_button').fadeToggle();
   

});
 $('.add_more .more_button').click(function(){
   $('.add_more .info').fadeToggle();
   

});


 /* end edit div */
   $('.sigin1 .tit1').click(function(){
    $('.sigin1 .ul').fadeToggle();
    $('.sigin1 .list').fadeToggle();
   

});

$('.pass1 h1').click(function(){
  $('.p').fadeToggle();

    
});
$('.link h1').click(function(){
  $('.one').fadeToggle();
  $('.sigin1').hide();
    
});

$('.link h2').click(function(){
  $('.sigin1').fadeToggle();
  $('.one').hide();
    
});
$('#nav').click(function(){
  $('.nav').fadeToggle();
  
    
});


      


});