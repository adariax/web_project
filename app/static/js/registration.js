const domen = "http://85f6ffb6.ngrok.io";

window.onload = getAccessToken();

function vk_login() {
    let uri = domen + '/end_registration';
    console.log(uri);
    if (validate() == true) {
        window.location.href = `https://oauth.vk.com/authorize?client_id=7367858&redirect_uri=${uri}&display=popup&scope=offline,wall,groups&response_type=token&revoke=1`;
    }
}

function validate() {
    let login = document.getElementById('login').value;
    let password = document.getElementById('password').value;
    let password_again = document.getElementById('password_a').value;

    if (login.length == 0) {
        if ($('#error-l-empty').length == 0) {
            let error = createError('Поле не заполнено');
            $(error).attr('id', 'error-l-empty');
            $('#login-div').append(error);
        }
        return false
    } else {
        $('#error-l-empty').remove();
    }

    if (password.length == 0) {
        if ($('#error-p-empty').length == 0) {
            let error = createError('Поле не заполнено');
            $(error).attr('id', 'error-p-empty');
            $('#password-div').append(error);
        }
        return false
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
        return false
    }).fail(function () {
        $('#error-login').remove();
    });

    if (password != password_again) {
        if ($('#error-password').length == 0) {
            let error = createError('Пароли не совпадают');
            error.attr('id', 'error-password');
            $('#password-div').append(error);
        }
        return false
    } else {
        $('#error-password').remove();
    }
    return true
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

function getAccessToken() {
    if (window.location.hash != '') {
        let hash = window.location.hash.slice(1).split('&');
        let access_token = hash[0];
        let user_id = hash[2];
        console.log(hash);
        $.ajax({
                url: "/api/access_token",
                type: 'POST',
                data: {
                    'access_token': access_token.split('=')[1],
                    'user_id': user_id.split('=')[1]
                }
            }
        )
    }
}