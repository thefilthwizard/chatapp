$(() => {
  $('#send').click(() => {
    sendMessage({
      id: 999,
      name: $('#name').val(),
      message: $('#message').val()
    })
    getMessages()
  })
})

const socket = io()

socket.on('message', getMessages)

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

function sendMessage(message) {
    $.post('http://192.243.100.152:8099/msg', message)
}
