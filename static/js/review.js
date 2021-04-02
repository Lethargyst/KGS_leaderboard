function render_last_one() {
            $.post('/review_rendering', {
                iteration: document.getElementById('iteration').innerHTML,
                action: '-'
            }).done(function(response) {
                d = new Date();
                $("#board").attr("src", "/static/img/board.png?"+d.getTime());
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
                d = new Date();
                $("#board").attr("src", "/static/img/board.png?"+d.getTime());
                document.getElementById('iteration').innerHTML = response.iteration
            }).fail(function() {
                $('#iteration').text("{{ _('Error: Could not contact server.') }}");
            });
        }
