const domain = "https://cd50891f.ngrok.io";

window.onload = registration();

function vk_login() {
    let uri = domain + '/registration';
    let clientId = $('#clientId').text();
    let login = document.getElementById('login').value;
    let encoder = new TextEncoder();
    let uint8Array = encoder.encode(login);
    if (validate() === true) {
        window.location.href = `https://oauth.vk.com/authorize?client_id=${clientId}&redirect_uri=${uri}&display=popup&scope=offline,wall,groups,photos&response_type=token&revoke=1&state=${uint8Array}`;
    }
}

function validate() {
    let login = document.getElementById('login').value;
    let validation = true;

    if (login.length === 0) {
        if ($('#error-l-empty').length === 0) {
            let error = createError('Поле не заполнено');
            $(error).attr('id', 'error-l-empty');
            $('#login-div').append(error);
        }
        validation = false
    } else {
        $('#error-l-empty').remove();
    }

    $.ajax({
            url: `/api/user/login/${login}`,
            type: 'GET',
        }
    ).done(function () {
        if ($('#error-login').length === 0) {
            let error = createError('Пользователь с таким логином существует');
            $(error).attr('id', 'error-login');
            $('#login-div').append(error);
        }
    }).fail(function () {
        $('#error-login').remove();
    });

    if ($('#error-login').length) {
        validation = false
    }
    return validation
}

function createError(message) {
    let error = document.createElement('div');
    error.classList.add('alert');
    error.classList.add('alert-danger');
    error.setAttribute('role', 'alert');
    error = $(error);
    error.text(message);
    return error
}

function registration() {
    if (window.location.hash !== '') {
        let info = getInfo();
        if (info) {
            $.ajax({
                url: '/api/users',
                type: 'POST',
                enctype : 'multipart/form-data',
                data: {
                    'nickname': info['login'],
                    'accessToken': info['accessToken'],
                    'vkDomain': info['vkDomain'],
                }
            }).done(function () {
                window.location.href = domain + '/login'
            }).fail(function () {
                alert('Этот аккаунт уже зарегистрирован');
            });
        }
    }
}

function getInfo() {
    let hash = window.location.hash.slice(1).split('&');
    window.location.hash = '';
    let accessToken = hash[0].split('=')[1];
    let userId = hash[2].split('=')[1];
    let loginUtf8 = new Uint8Array(hash[3].split('=')[1].split(',').map(n => parseInt(n, 10)));
    let decoder = new TextDecoder();
    let login = decoder.decode(loginUtf8);
    return {
        'login': login,
        'accessToken': accessToken,
        'vkDomain': userId,
    }
}