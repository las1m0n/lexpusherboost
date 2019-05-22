//go top button
$(document).ready(function()
{
    $(window).scroll(function()
    {
        if ($(this).scrollTop() > 100)
        {$('.scrollup').fadeIn();} else {
        $('.scrollup').fadeOut();}
    });
    $('.scrollup').click(function()
    {$("html, body").animate({scrollTop: 0}, 500);return false;
    });
});


 $(document).ready(function(){
    $("#menu").on("click","a", function (event) {
        event.preventDefault();
        var id  = $(this).attr('href'),
            top = $(id).offset().top;
        $('body,html').animate({scrollTop: top}, 500);
    });
});


$(document).ready(function() {
  $("a.scrollto").click(function() {
    var elementClick = $(this).attr("href")
    var destination = $(elementClick).offset().top;
    jQuery("html:not(:animated),body:not(:animated)").animate({
      scrollTop: destination
    }, 800);
    return false;
  });
});
