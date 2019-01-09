getMessages()

$(() => {
  $('#send').click(() => {
    sendMessage({
      id: 999,
      name: $('#name').val(),
      message: $('#message').val()
    })
    latestMsg()
    $('#message').empty()
  })
})

const socket = io()

socket.on('message', () => {
  console.log('get emmit from socket.io')
  latestMsg()
})

function addMessages(message) {
  $('#messages').append(`
    <h4> ${message.name} </h4>
    <p>  ${message.message} </p>`)
}

function getMessages() {
  $('#messages').empty()
  $.get('http://192.243.100.152:8099/call', (data) => {
    data.forEach(addMessages)
  })
  window.scrollTo(0, document.body.scrollHeight)
}

function latestMsg() {
  $.get('http://192.243.100.152:8099/call', (data) => {
    const lastMsg = data[data.length - 1]
    addMessages(lastMsg)
  })
  window.scrollTo(0, document.body.scrollHeight)
}  

function sendMessage(message) {
    $.post('http://192.243.100.152:8099/msg', message)
}
