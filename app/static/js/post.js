let attachment = null;
let reader = new FileReader();
let imgInput = $("#image");
imgInput.change(function (event) {
    let file = event.target.files[0];
    reader.readAsDataURL(file);
    reader.onload = function () {
        $.ajax({
            url: '/api/posts/picture',
            type: 'POST',
            data: {'image': reader.result},
            async: false,
            success: function (data) {
                attachment = data.attachment
            },
            fail: function () {
            }
        })
    }
});


function createPost() {
    let ownerId = $("#group_id").text();
    let message = $("#description").val();
    let datetime = $('#datetime');
    let fromGroup = $('#fromGroup').is(':checked');
    let signed = $('#signed').is(':checked');
    let unix = 0;
    if ( message === '' || attachment === null ) {
        $('.row').remove('.alert');
        if ((datetime.length !== 0) && !(datetime.text() === '')) {
            unix = getUnix(-1 * (new Date().getTimezoneOffset() / 60));
        }
        if (unix === false) {
            if ($('.alert').length === 0) {
                createError('Неверный формат ввода даты/времени публикации');
                return
            }
        }
        VK.Api.call('wall.post', {
                owner_id: parseInt(ownerId, 10),
                message: message,
                publish_date: unix,
                attachments: attachment,
                from_group: Number(fromGroup),
                signed: Number(signed),
                v: "5.103"
            },
            function (r) {
                console.log(r);
                window.location.href = '/'
            })
    } else {
        if ($('.alert').length === 0) {
            createError('Пустой пост опубликовать невозможно')
        }
    }

}

function createError(message) {
    let error = document.createElement('div');
    error.classList.add('alert');
    error.classList.add('alert-secondary');
    error.setAttribute('role', 'alert');
    error.setAttribute('style', 'width: 100%; align-content: center');
    error = $(error);
    error.text(message);
    $('.row').append(error)
}


function getUnix(tz) {
    let datetime = $('#datetime').val().split(' ');
    let date = datetime[0];
    let time = datetime[1];
    let unix = 0;
    console.log(tz.toString());
    $.ajax({
        url: `/api/posts/unixtime_${date}_${time}_${tz.toString()}`,
        type: 'GET',
        global: false,
        async: false,
        success: function (data) {
            unix = data.unixtime
        },
    }).fail(function () {
        unix = false
    });
    return unix
}