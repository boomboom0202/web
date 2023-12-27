function toggleForm(showFormId, hideFormId) {
    $('#' + showFormId + 'Container').show();
    $('#' + hideFormId + 'Container').hide();

    $('.toggle-buttons button').removeClass('active');
    $('#' + showFormId.replace('Form', 'Button')).addClass('active');

    // Очистим сообщения при переключении форм
    document.getElementById('message').innerHTML = '';
    document.getElementById('registerMessage').innerHTML = '';
}

function authenticate() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    $.ajax({
        type: 'POST',
        url: '/authenticate',
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify({ email: email, password: password }),
        success: function (data) {
            // Сохраняем токен в localStorage
            localStorage.setItem('accessToken', data.token);
            
            // Перенаправление на защищенную страницу при успешной аутентификации
            window.location.href = '/index';
        },
        error: function (error) {
            document.getElementById('message').innerHTML = 'Authentication failed. Check your credentials.';
        }
    });
}

function accessSecuredPage() {
    const accessToken = localStorage.getItem('accessToken');

    $.ajax({
        type: 'GET',
        url: '/index',
        headers: {
            Authorization: `Bearer ${accessToken}`
        },
        success: function (data) {
            // Обработка успешного получения защищенной страницы
        },
        error: function (error) {
            // Обработка ошибки доступа к защищенной странице
            if (error.status === 401) {
                // Перенаправление на страницу аутентификации или другую страницу с сообщением об ошибке
                window.location.href = '/login?error=unauthorized';
            } else {
                // Обработка других ошибок доступа
            }
        }
    });
}
function register() {
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;

    $.ajax({
        type: 'POST',
        url: '/register',
        contentType: 'application/json;charset=UTF-8',
        data: JSON.stringify({ email: email, password: password }),
        success: function (data) {
            document.getElementById('registerMessage').innerHTML = data.message;
        },
        error: function (error) {
            document.getElementById('registerMessage').innerHTML = 'Registration failed. Check your input.';
        }
    });
}
