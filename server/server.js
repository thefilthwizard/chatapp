const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
// const spawn = require('child_process').spawn;
// const fs = require('fs');
const http = require('http').Server(app);
const io = require('socket.io')(http);
const path = require('path');
// const ltunnel = require('localtunnel');
require('https').globalAgent.options.ca = require('ssl-root-cas/latest').create();

app.use(express.static('public'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
  extended: false
}));

const Message = mongoose.model('Message', {
  id: Number,
  name: String,
  message: String
});

const dbUrl = 'mongodb://localhost:27017/dirtychat'; // setup mongo db

mongoose.connect(dbUrl, { useNewUrlParser: true }, (err) => {
  io.emit('mongodbconnected');
  console.log('MongoDB Error: ', err);
});

io.on('connection', () => {
  io.emit('userconnected');
});

app.post('/msg', (req, res) => {
  try {
    const message = new Message(req.body);
    const savedMessage = message.save((err) => {
      res.sendStatus(200);
      console.log(err);
    });
    console.log(savedMessage);
  } catch (error) {
    res.sendStatus(500);
    return console.log('post error:' + error);
  } finally {
    console.log('Message Posted');
    io.emit('message');
  }
});

app.get('/messages/:user', (req, res) => {
  const user = req.params.user;
  Message.find({ name: user }, (err, messages) => {
    res.send(messages);
    console.log(err);
  });
});

app.get('/call', (req, res) => {
  const msgID = req.params.id;
  Message.find({ id: msgID }, (err, messages) => {
    res.send(messages);
    console.log(err);
  });
});

app.get('/ping', (req, res) => {
  res.sendStatus(200);
});

app.get('/', (req, res) => {
  const pathToIndex = path.join(__dirname, '/public/', 'index.html');
  res.sendFile(pathToIndex);
});

const server = http.listen(8099, () => {
  const host = server.address().address;
  const port = server.address().port;
  console.log('listening on host: ' + host + ' port no: ' + port);
});

/* const tunnel = ltunnel(8099, { subdomain: 'filthwizard' }, (err, tun) => {
   if (err) console.log('tunnel error: ' + err);
   let puburl = tun.url;
   console.log('puburl: ' + puburl + '\n');
});

tunnel.on('close', () => {
   console.log('pub tunnel is closed\n');
}); */
