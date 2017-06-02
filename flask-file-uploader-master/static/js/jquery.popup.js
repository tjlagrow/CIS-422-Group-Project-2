// Popup Window
var scrollTop = '';
var newHeight = '100';

$(window).bind('scroll', function() {
    scrollTop = $( window ).scrollTop();
    newHeight = scrollTop + 100;
});

$('.popup-trigger').click(function(e) {
    e.stopPropagation();
    if(jQuery(window).width() < 767) {
        $(this).after( $( ".popup" ) );
        $('.popup').show().addClass('popup-mobile').css('top', 0);
        $('html, body').animate({
            scrollTop: $('.popup').offset().top
        }, 500);
    } else {
        $('.popup').removeClass('popup-mobile').css('top', newHeight).toggle();
    };
});

$('html').click(function() {
    $('.popup').hide();
});

$('.popup-btn-close').click(function(e){
    $('.popup').hide();
});

$('.popup').click(function(e){
    e.stopPropagation();
});

// Popup1 Window
var scrollTop = '';
var newHeight = '100';

$(window).bind('scroll', function() {
    scrollTop = $( window ).scrollTop();
    newHeight = scrollTop + 100;
});

$('.popup-trigger1').click(function(e) {
    e.stopPropagation();
    if(jQuery(window).width() < 767) {
        $(this).after( $( ".popup1" ) );
        $('.popup1').show().addClass('popup-mobile1').css('top', 0);
        $('html, body').animate({
            scrollTop: $('.popup1').offset().top
        }, 500);
    } else {
        $('.popup1').removeClass('popup-mobile1').css('top', newHeight).toggle();
    };
});

$('html').click(function() {
    $('.popup1').hide();
});

$('.popup-btn-close').click(function(e){
    $('.popup1').hide();
});

$('.popup1').click(function(e){
    e.stopPropagation();
});
