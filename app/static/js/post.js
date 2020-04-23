let ownerId = $("#groupId").text();
let postId = null;
let attachment = null;

window.onload = getData();

let reader = new FileReader();
let imgInput = $("#image");
let button = $('#post');

imgInput.change(function (event) {
    button.text('Дождитесь окончания загрузки');
    button.prop('disabled', true);

    let file = event.target.files[0];
    reader.readAsDataURL(file);
    reader.onload = function () {
        $.ajax({
            url: '/api/posts/picture',
            type: 'POST',
            data: {'image': reader.result},
            success: function (data) {
                attachment = data.attachment
            },
            fail: function () {
            }
        }).always(function () {
            button.text('Отправить');
            button.prop('disabled', false);
        })
    };
});


function createPost() {
    let message = $("#description").val();
    let datetime = $('#datetime');
    let fromGroup = $('#fromGroup').is(':checked');
    let signed = $('#signed').is(':checked');
    let unix = null;
    if (message !== '' || attachment !== null) {
        $('#contPost').remove('.alert');
        if (datetime.length !== 0) {
            unix = getUnix(-1 * (new Date().getTimezoneOffset() / 60));
        }
        if (unix != null && unix < Number((new Date().getTime()).toString().slice(0, 10))) {
            if ($('.alert').length === 0) {
                createError('Неверный формат ввода даты/времени публикации');
            }
            return
        }
        unix = 0;
        let params = {
            owner_id: Number(ownerId),
            message: message,
            publish_date: unix,
            attachments: attachment,
            from_group: Number(fromGroup),
            signed: Number(signed),
            v: "5.103"
        };
        if (postId !== null) {
            params.post_id = postId;
        }
        VK.Api.call('wall.post', params,
            function (resp) {
                if (resp.error === undefined){
                    window.location.href = '/'
                }
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
    error.setAttribute('style', 'width: 100%; margin-top: 1vh');
    error = $(error);
    error.text(message);
    $('#contPost').append(error)
}


function getUnix(tz) {
    let datetime = $('#datetime').val().split(' ');
    let date = datetime[0];
    let time = datetime[1];
    let unix = 0;
    $.ajax({
        url: `/api/posts/unixtime_${date}_${time}_${tz.toString()}`,
        type: 'GET',
        global: false,
        async: false,
        success: function (data) {
            unix = data.unixtime
        },
    }).fail(function () {
        unix = 0
    });
    return unix
}

function getData() {
    if (window.location.hash !== '') {
        $('#contPost').removeClass('row');
        $('#image').remove();
        $('#fromGroup').attr("checked", "checked");
        $('#fromGroup').prop('disabled', true);
        $('#signed').attr("checked", "checked");

        postId = window.location.hash.slice(1);
        VK.Api.call('wall.getById', {
            posts: `${ownerId}_${postId}`,
            v: "5.103"
        }, function (data) {
            $("#description").text(data.response[0].text);
            if (data.response[0].attachments.length > 1) {
                createError('ВНИМАНИЕ. ' +
                    'Количество медиа-объектов этого поста больше одной фотографии. ' +
                    'Рекомендуем Вам продолжить подготовку публикации в Вашей группе ВКонтакте, ' +
                    'чтобы избежать потери данных.')
            }

            let image = document.createElement('img');
            image.setAttribute('src', data.response[0].attachments[0].photo.sizes[3].url);
            image.setAttribute('style', 'float: right; margin-top: 1vh; self-align: center');
            $(image).insertAfter($('#description'));

            attachment = `photo${ownerId}_${data.response[0].attachments[0].photo.id}`;
        })
    }
}