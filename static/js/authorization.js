function authorization () {
     $.post('/check_authorization', {
                name: '',
                password: ''
            }).fail(function() {
                $('#iteration').text("Неверный логин или пароль");
            });
        }
}