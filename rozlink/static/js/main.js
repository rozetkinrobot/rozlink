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

var rootEl = document.documentElement;
var $modals = getAll('.modal');
var $modalButtons = getAll('.modal-button');
var $modalCloses = getAll('.modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button');
var $clipboardButtons = getAll('.clipboad-button');
var $passButtons = getAll('.toggle-pass');

if ($modalButtons.length > 0) {
    $modalButtons.forEach(function (el) {
        $(el).click(() => {
            var target = el.dataset.target;
            if ($(el).hasClass("modal-link-button")) {
                var link_id = el.dataset.linkid;
                prepareModal(target, link_id);
            }
            else {
                openModal(target);
            }
        });
    });
}

if ($clipboardButtons.length > 0) {
    $clipboardButtons.forEach(function (el) {
        $(el).click(() => {
            var target = el.dataset.target;
            clipboard_click(target, el);
        });
    });
}

if ($passButtons.length > 0) {
    $passButtons.forEach(function (el) {
        $(el).click(() => {
            var target = el.dataset.target;
            toggle_Pass(target, el);
        });
    });
}

if ($modalCloses.length > 0) {
    $modalCloses.forEach(function (el) {
        $(el).click(() => {
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
    $modals.forEach(function (el) {
        el.classList.remove('is-active');
    });
}

document.addEventListener('keydown', function (event) {
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


function prepareModal(target, link_id) {
    // var $target = document.getElementById(target);
    var data = { "id": link_id };

    var jqxhr = $.ajax({
        type: 'POST',
        contentType: "application/json",
        accepts: "application/json",
        cache: false,
        dataType: 'json',
        data: JSON.stringify(data),
        url: '/api/v1/link_info',
    });


    jqxhr.done(function (data, textStatus, jqXHR) {
        var response_data = data["data"];
        $("#large_link").val(response_data["ll"]);
        $("#short_link").val(response_data["sl"]);
        $("#views_table").empty();

        var state = response_data["is_active"];
        $("#status_button_control").empty();
        if (state) {
            $("#status_button_control").append('<button class="button is-link" id="status_button" data-status="on">Active</button>');
        }
        else {
            $("#status_button_control").append('<button class="button is-danger" id="status_button" data-status="off">Deactive</button>');
        }
        $(() => {
            $("#status_button").click(() => {
                link_status(link_id);
            });
            $("#delete_link_button").off()
            $("#delete_link_button").click(() => {
                delete_link(link_id);
            });
        });
        $("#qr_code").attr("src", "https://api.qrserver.com/v1/create-qr-code/?size=128x128&data=" + response_data["sl"]);

        var views = response_data["views"];
        for (i in views) {
            $("#views_table").append("<tr><td>" + views[i]["ip"] + "</td><td>" + views[i]["time"] + "</td></tr>")
        }
        openModal(target)
    });

    jqxhr.fail(function (jqXHR, textStatus, errorThrown) {
        console.log('Failed:', errorThrown);
    });
}

function link_status(link_id) {
    $("#status_button").toggleClass("is-loading")
    var status = $("#status_button").data(status);

    if (status["status"] == "on") {
        var data = { "id": link_id, "state": 0 };
    }
    else {
        var data = { "id": link_id, "state": 1 };
    }

    var jqxhr = $.ajax({
        type: 'POST',
        contentType: "application/json",
        accepts: "application/json",
        cache: false,
        dataType: 'json',
        data: JSON.stringify(data),
        url: '/api/v1/set_link_state',
    });
    jqxhr.done(function (data, textStatus, jqXHR) {
        var new_state = data["data"]["is_active"];
        $("#status_button_control").empty();
        if (new_state) {
            $("#status_button_control").append('<button class="button is-link" id="status_button" data-status="on">Active</button>');
        }
        else {
            $("#status_button_control").append('<button class="button is-danger" id="status_button" data-status="off">Deactive</button>');
        }
        $(() => {
            $("#status_button").click(() => {
                link_status(link_id)
            });
        });
    });
    jqxhr.fail(function (jqXHR, textStatus, errorThrown) {
        console.log('Failed:', errorThrown);
    });
}

function delete_link(link_id) {
    $("#delete_link_button").toggleClass("is-loading")
    var status = $("#status_button").data(status);
    var data = { "id": link_id };

    var jqxhr = $.ajax({
        type: 'POST',
        contentType: "application/json",
        accepts: "application/json",
        cache: false,
        dataType: 'json',
        data: JSON.stringify(data),
        url: '/api/v1/delete_link',
    });
    jqxhr.done(function (data, textStatus, jqXHR) {
        $("#delete_link_button").toggleClass("is-loading")
        closeModals();
        $("#link-id-" + link_id).remove()
    });
    jqxhr.fail(function (jqXHR, textStatus, errorThrown) {
        console.log('Failed:', errorThrown);
    });
}



function clipboard_click(target, button) {
    var copyText = document.getElementById(target);
    copyText.select();
    copyText.setSelectionRange(0, 99999);
    document.execCommand("copy");

    button.classList.remove("fa-clipboard-list")
    button.classList.add("fa-clipboard-check")
    button.classList.add("is-success")
    setTimeout(() => {
        button.classList.remove("fa-clipboard-check");
        button.classList.remove("is-success");
        button.classList.add("fa-clipboard-list")
    }, 2000);
}

function toggle_Pass(target, button) {
    $(button).toggleClass("fa-eye");
    $(button).toggleClass("fa-eye-slash");
    const type = $("#" + target).attr('type');
    $("#" + target).attr(
        'type', type === 'password' ? 'text' : 'password');
}
