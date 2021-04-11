$(function() {
    $(document).on('click', '.delete', function() {
        $(this).parents(".message").slideUp(400, function() {
            $(this).parents(".message").remove();
        });
    });
    $(document).on('click', '.toggle-pass', function() {
        // console.log($(this));
        const eye_pos = $(this).hasClass("fa-eye");
        // console.log(eye_pos);
        $(this).addClass(eye_pos == true ? "fa-eye-slash" : "fa-eye")
        $(this).removeClass(eye_pos == true ? "fa-eye" : "fa-eye-slash")
        const type = $("#password").attr('type');
        $("#password").attr(
            'type', type === 'password' ? 'text' : 'password');
    });
});