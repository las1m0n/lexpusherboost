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

// fade scroll navbar
 $(document).ready(function(){
    $("#menu").on("click","a", function (event) {
        event.preventDefault();
        var id  = $(this).attr('href'),
            top = $(id).offset().top;
        $('body,html').animate({scrollTop: top}, 500);
    });
});
