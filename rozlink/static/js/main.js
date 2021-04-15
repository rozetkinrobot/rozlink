// burger mobile

$(() => {
    $(".navbar-burger").click(() => {
        $(".navbar-burger").toggleClass("is-active");
        $(".navbar-menu").toggleClass("is-active");
    });
});


// messages deleting

$(document).on('click', '.delete', function() {
    $(this).parents(".message").slideUp(400, function() {
        $(this).parents(".message").remove();
    });
});

//pass toggle
$(document).on('click', '.toggle-pass', function() {
    const eye_pos = $(this).hasClass("fa-eye");
    $(this).addClass(eye_pos == true ? "fa-eye-slash" : "fa-eye")
    $(this).removeClass(eye_pos == true ? "fa-eye" : "fa-eye-slash")
    const type = $("#password").attr('type');
    $("#password").attr(
        'type', type === 'password' ? 'text' : 'password');
});

var rootEl = document.documentElement;
var $modals = getAll('.modal');
var $modalButtons = getAll('.modal-button');
var $modalCloses = getAll('.modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button');

if ($modalButtons.length > 0) {
    $modalButtons.forEach(function($el) {
        $el.addEventListener('click', function() {
            var target = $el.dataset.target;
            openModal(target);
        });
    });
}

if ($modalCloses.length > 0) {
    $modalCloses.forEach(function($el) {
        $el.addEventListener('click', function() {
            closeModals();
        });
    });
}

function openModal(target) {
    var $target = document.getElementById(target);
    rootEl.classList.add('is-clipped');
    $target.classList.add('is-active');
}

function closeModals() {
    rootEl.classList.remove('is-clipped');
    $modals.forEach(function($el) {
        $el.classList.remove('is-active');
    });
}

document.addEventListener('keydown', function(event) {
    var e = event || window.event;

    if (e.keyCode === 27) {
        closeModals();
        closeDropdowns();
    }
});

function getAll(selector) {
    var parent = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : document;

    return Array.prototype.slice.call(parent.querySelectorAll(selector), 0);
}