getMessages();
$(() => {
    $("#send").click(()=>{
       sendMessage({
            id: 999,
            name: $("#name").val(), 
            message:$("#message").val()});
        getMessages();
    });    
}); 

let socket = io();

socket.on('message', addMessages);

function addMessages(message){
    $('#messages').append(`
        <h4> ${message.name} </h4>
        <p>  ${message.message} </p>`);
}

function getMessages(){
    $('#messages').empty();
    $.get('https://filthwizzard.localtunnel.me/call', (data) => {
        data.forEach(addMessages);
    });
}

function sendMessage(message){
    $.post('https://filthwizzard.localtunnel.me/msg', message);
}