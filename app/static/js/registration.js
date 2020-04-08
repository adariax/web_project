function vk_login() {
    console.log('a');
    let uri = + '/end_registration';
    if (validate() == true) {
        window.location.href = `https://oauth.vk.com/authorize?client_id=7367858&display=popup&scope=offline,wall,groups&response_type=token&redirect_url=${uri}`;
    }
}

function validate() {
    let login = document.getElementById('login').value;
    let password = document.getElementById('password').value;
    let password_again = document.getElementById('password_a').value;
    return false
}

function createError(message) {
    let error = document.createElement('div');
    error.classList.add('alert');
    error.classList.add('alert-danger');
    error.setAttribute('role', 'alert');
    error.innerText = message;
    return error
}