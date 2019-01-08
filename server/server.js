const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
//const spawn = require('child_process').spawn;
//const fs = require('fs');
const http = require('http').Server(app);
const io = require('socket.io')(http);
const ltunnel = require('localtunnel');
require('https').globalAgent.options.ca = require('ssl-root-cas/latest').create();

app.use(express.static('public'));
app.use( bodyParser.json() );       
app.use(bodyParser.urlencoded({     
  extended: false
})); 

let Message = mongoose.model('Message', {
   id: Number,
   name : String,
   message : String
});

let dbUrl = 'mongodb://localhost:27017/dirtychat'; // setup mongo db

mongoose.connect(dbUrl, { useNewUrlParser: true }, (err) => {
   console.log('mongodb connected', err);
});

io.on('connection', () => {
   console.log('a user is connected');
});

app.post('/msg', (req, res) => {
   try{
      let message = new Message(req.body);  
      let savedMessage = message.save( (err) => {
         res.sendStatus(200);
      });   
    }
    catch (error) {
      res.sendStatus(500);
      return console.log('post error:' + error);
    }
    finally{
      console.log('Message Posted');
    }
 });

 app.get('/messages/:user', (req, res) => {
   let user = req.params.user;
   Message.find({name: user},(err, messages)=> {
     res.send(messages);
   });
 });

app.get('/call', (req, res) => {
  Message.find({},(err, messages)=> {
      res.send(messages);
   });
});

app.get('/ping', (req, res) => {
   res.sendStatus(200);
});   

app.get('/', (req, res) => {
   res.sendFile( __dirname + '/public/' + 'index.html' );
});

const server = http.listen(8099, () => {
   const host = server.address().address;
   const port = server.address().port;
});

const tunnel = ltunnel(8099, { subdomain: 'filthwizard' }, (err, tun) => {
   if (err) console.log('tunnel error: ' + err);
   let puburl = tun.url;
   console.log('puburl: ' + puburl + '\n');
});

tunnel.on('close', () => {
   console.log('pub tunnel is closed\n');
});