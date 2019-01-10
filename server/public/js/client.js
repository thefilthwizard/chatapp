const msgDiv = document.getElementById('messages');
const socket = io();

$(document).onload(() => {
  getMessages();
  msgDiv.scrollTop = msgDiv.scrollHeight;
});

$(() => {
  $('#send').click(() => {
    sendMessage({
      id: 999,
      name: $('#name').val(),
      message: $('#message').val()
    });
    $('#message').empty();
  });
});

socket.on('message', () => {
  console.log('get emmit from socket.io');
  latestMsg();
});

function addMessages(message) {
  $('#messages').append(`
    <h4> ${message.name} </h4>
    <p>  ${message.message} </p>`);
}

function getMessages() {
  $('#messages').empty();
  $.get('http://192.243.100.152:8099/call', (data) => {
    data.forEach(addMessages);
  });
}

function latestMsg() {
  $.get('http://192.243.100.152:8099/call', (data) => {
    const lastMsg = data[data.length - 1];
    addMessages(lastMsg);
  });
  msgDiv.scrollTop = msgDiv.scrollHeight;
}

function sendMessage(message) {
    $.post('http://192.243.100.152:8099/msg', message);
}
