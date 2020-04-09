const domain = "https://f6454672.ngrok.io";

window.onload = registration();

function vk_login() {
    let uri = domain + '/registration';
    let login = document.getElementById('login').value;
    let password = document.getElementById('password').value;
    if (validate() == true) {
        window.location.href = `https://oauth.vk.com/authorize?client_id=7367858&redirect_uri=${uri}&display=popup&scope=offline,wall,groups&response_type=token&revoke=1&state=${login},${password}`;
    }
}

function validate() {
    let login = document.getElementById('login').value;
    let password = document.getElementById('password').value;
    let password_again = document.getElementById('password_a').value;

    let validation = true;

    if (login.length == 0) {
        if ($('#error-l-empty').length == 0) {
            let error = createError('Поле не заполнено');
            $(error).attr('id', 'error-l-empty');
            $('#login-div').append(error);
        }
        validation = false
    } else {
        $('#error-l-empty').remove();
    }

    if (password.length == 0) {
        if ($('#error-p-empty').length == 0) {
            let error = createError('Поле не заполнено');
            $(error).attr('id', 'error-p-empty');
            $('#password-div').append(error);
        }
        validation = false
    } else {
        $('#error-p-empty').remove();
    }

    $.ajax({
            url: `/api/user/login/${login}`,
            type: 'GET',
        }
    ).done(function () {
        if ($('#error-login').length == 0) {
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

    if (password != password_again) {
        if ($('#error-password').length == 0) {
            let error = createError('Пароли не совпадают');
            error.attr('id', 'error-password');
            $('#password-div').append(error);
        }
        validation = false
    } else {
        $('#error-password').remove();
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
    if (window.location.hash != '') {
        let info = getInfo();
        if (info) {
            $.ajax({
                url: '/api/users',
                type: 'POST',
                data: {
                    'nickname': info['login'],
                    'password': info['password'],
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
    let regInfo = hash[3].split('=')[1].split(',');
    let login = regInfo[0];
    let password = regInfo[1];
    return {
        'login': login,
        'password': password,
        'accessToken': accessToken,
        'vkDomain': userId,
    }
}