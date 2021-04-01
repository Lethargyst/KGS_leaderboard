$(document).ready(function(){
  $(".button").click(function(){
    $(".collapse").collapse('hide');
  });
});


function get_user_info(user) {
            $.post('/info', {
                user_name: user
            }).done(function(response) {
                var container = document.getElementById('table_{user}'.replace('{user}', user)).getElementsByTagName('tbody')[0];

                var gamesArr = response.games
                for(var i=0; i < gamesArr.length; i++){
                    var game = gamesArr[i]
                    var tr = document.createElement('tr');

                    var gameNum = document.createElement('th');
                    gameNum.innerHTML = game.num;
                    gameNum.rowSpan = game.users_amount;

                    var gameScore = document.createElement('td')
                    gameScore.innerHTML = game.score;
                    gameScore.rowSpan = game.users_amount;

                    var gameDuration = document.createElement('td');
                    gameDuration.innerHTML = game.duration;
                    gameDuration.rowSpan = game.users_amount;

                    var userName = document.createElement('td');
                    userName.innerHTML = user;

                    var userColor = document.createElement('td');
                    userColor.innerHTML = game.users[0].color;

                    tr.appendChild(gameNum);
                    tr.appendChild(userName);
                    tr.appendChild(userColor);
                    tr.appendChild(gameScore);
                    tr.appendChild(gameDuration);

                    container.appendChild(tr);

                    for(var j=1; j < game.users.length; j++){
                        var tr = document.createElement('tr');

                        var userName = document.createElement('td');
                        userName.innerHTML = game.users[j].name;

                        var userColor = document.createElement('td');
                        userColor.innerHTML = game.users[j].color;

                        tr.appendChild(userName);
                        tr.appendChild(userColor);

                        container.appendChild(tr);
                    };

               $("#collapse-{user}".replace('{user}', user)).collapse('show');

                };
            }).fail(function() {
                $("#collapse-{user}".replace('{user}', user)).collapse('toggle');
            });
        }

