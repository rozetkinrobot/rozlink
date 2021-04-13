// burger mobile

$(() => {
    $(".navbar-burger").click(() => {
        $(".navbar-burger").toggleClass("is-active");
        $(".navbar-menu").toggleClass("is-active");
    });
});


// messages deleting

$(document).on('click', '.delete', function () {
    $(this).parents(".message").slideUp(400, function () {
        $(this).parents(".message").remove();
    });
});

//pass toggle
$(document).on('click', '.toggle-pass', function () {
    const eye_pos = $(this).hasClass("fa-eye");
    $(this).addClass(eye_pos == true ? "fa-eye-slash" : "fa-eye")
    $(this).removeClass(eye_pos == true ? "fa-eye" : "fa-eye-slash")
    const type = $("#password").attr('type');
    $("#password").attr(
        'type', type === 'password' ? 'text' : 'password');
});