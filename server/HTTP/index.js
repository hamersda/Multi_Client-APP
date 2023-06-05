const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const port = 8000;

const db = require('./queries');

app.use(bodyParser.json());
app.use(
  bodyParser.urlencoded({
    extended: true,
  })
);

app.get('/', (request, response) => {
  response.json({ info: 'Node.js, Express, and Postgres API' });
});

app.get('/users', db.authenticateToken, db.getUsers);
app.get('/users/:id', db.authenticateToken, db.getUserById);
app.post('/register', db.createUser);
app.put('/users/:id', db.authenticateToken, db.updateUser);
app.delete('/users/:id', db.authenticateToken, db.deleteUser);
app.get('/messages', db.authenticateToken, db.getMessage);
app.get('/messages/:id', db.authenticateToken, db.getMessageById);
app.post('/messages', db.authenticateToken, db.createMessage);
app.put('/messages/:id', db.authenticateToken, db.updateMessage);
app.delete('/messages/:id', db.authenticateToken, db.deleteMessage);
app.get('/devices', db.authenticateToken, db.getDevice);
app.get('/devices/:id', db.authenticateToken, db.getDeviceById);
app.post('/devices', db.authenticateToken, db.createDevice);
app.put('/devices/:id', db.authenticateToken, db.updateDevice);
app.delete('/devices/:id', db.authenticateToken, db.deleteDevice);
app.post('/login', db.checkPassword);

app.listen(port, () => {
  console.log(`App running on port ${port}.`);
});