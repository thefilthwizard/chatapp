const msgDiv = document.getElementById('messages');
const socket = io();

$(window).on('load', () => {
  getMessages().then(autoScroll);  
});

function autoScroll() {
  msgDiv.style.overflow = 'hidden';
  msgDiv.scrollTop = msgDiv.scrollHeight;
  msgDiv.style.overflow = 'scroll';
}

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
  latestMsg().then(autoScroll);
});

function addMessages(message) {
  $('#messages').append(`
    <h4> ${message.name} </h4>
    <p>  ${message.message} </p>`);
}

function getMessages() {
  const sync = $.Deferred();
  $('#messages').empty();
  $.get('http://192.243.100.152:8099/call', (data) => {
    data.forEach(addMessages);
  });
  setTimeout(() => {
    sync.resolve();
  }, 500);
  return sync;
}

function latestMsg() {
  const sync = $.Deferred();
  $.get('http://192.243.100.152:8099/call', (data) => {
    const lastMsg = data[data.length - 1];
    addMessages(lastMsg);
  });
  setTimeout(() => {
    sync.resolve();
  }, 500);
  return sync;
}

function sendMessage(message) {
    $.post('http://192.243.100.152:8099/msg', message);
}
