var MIN = 1400;
var MAX = 2000;

var count = MIN;

var start = function (n, callback) {
  $.ajax({
  type: 'POST',
  url: "http://www.hackerrank.com/splash/challenge.json",
  data: {n: n, remote: true, utf8: true},
  success: callback,
  dataType: "json"
  });
};

var move = function (move, callback) {
  $.ajax({
  type: 'PUT',
  url: "http://www.hackerrank.com/splash/challenge.json",
  data: {move: move, remote: true, utf8: true},
  success: callback,
  dataType: "json"
  });
};

var play = function (data) {
  if (data == null) {
    if(count%6 == 0)
      count = count + 1;
    console.log(count);
    start(count, play);
    return;
  } else if (data.game == null) {
    move(data.current%6, play);
    return;
  } else if (data.game.solved === true) {
    count = count + 1;
    if(count%6 == 0)
      count = count + 1;
    if(count > MAX)
      return;
    play();
    return;
  } else {
    move(data.game.current%6, play);
  }
};