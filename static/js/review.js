function render_last_one() {
            $.post('/review_rendering', {
                iteration: document.getElementById('iteration').innerHTML,
                action: '-'
            }).done(function(response) {
                var sc_width = document.documentElement.clientWidth
                var sc_height = document.documentElement.clientHeight
                var board_size = Math.min(sc_width, sc_height) - 100
                d = new Date();
                $("#board").attr("src", "/static/img/board.png?"+d.getTime());
                document.getElementById('board').style.width = String(board_size) + 'px'
                document.getElementById('board').style.height = String(board_size) + 'px'
                document.getElementById('iteration').innerHTML = response.iteration
            }).fail(function() {
                $('#iteration').text("{{ _('Error: Could not contact server.') }}");
            });
        }

function render_next_one() {
            $.post('/review_rendering', {
                iteration: document.getElementById('iteration').innerHTML,
                action: '+'
            }).done(function(response) {
                var sc_width = document.documentElement.clientWidth
                var sc_height = document.documentElement.clientHeight
                var board_size = Math.min(sc_width, sc_height) - 100
                d = new Date();
                $("#board").attr("src", "/static/img/board.png?"+d.getTime());
                document.getElementById('board').style.width = String(board_size) + 'px'
                document.getElementById('board').style.height = String(board_size) + 'px'
                document.getElementById('iteration').innerHTML = response.iteration
            }).fail(function() {
                $('#iteration').text("{{ _('Error: Could not contact server.') }}");
            });
        }

window.onload = function set_size() {
    var sc_width = document.documentElement.clientWidth
    var sc_height = document.documentElement.clientHeight
    var board_size = Math.min(sc_width, sc_height) - 100
    document.getElementById('board').style.width = String(board_size) + 'px'
    document.getElementById('board').style.height = String(board_size) + 'px'
}