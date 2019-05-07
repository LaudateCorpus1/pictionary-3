var timer = 121;
var game_start = false;
var game_id = '';

$(function() {
    $('body').append($('<span class="ripple"></span>'));
    $('[data-toggle="tooltip"]').tooltip();
    $('#drawing-board').height($('#drawing-board').parent().height());
    $('#drawing-board').width($('#drawing-board').parent().width());

    $(".ripple").on('animationend webkitAnimationEnd oAnimationEnd oanimationend MSAnimationEnd', 
    function() {
    $('.ripple').removeClass('active');
    });

    var interval = setInterval(function() {
        --timer;
        
        if (timer == 60) {
            $('.countdown').addClass('blink-danger')
        }

        if (timer < 0) {
            clearInterval(interval);
            $('.timeup-card').toggleClass('show');
            finishGame();
        }

        timer = (timer < 0) ? 0 : timer;
        $('.countdown').html(timer);

    }, 1000);
});