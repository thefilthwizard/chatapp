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
    $.get('https://filthwizard.localtunnel.me/call', (data) => {
        data.forEach(addMessages);
    });
    
    window.scrollTo(0,document.body.scrollHeight);
}

function sendMessage(message){
    $.post('https://filthwizard.localtunnel.me/msg', message);
}