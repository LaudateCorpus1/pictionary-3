var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

app.get('/', function(req, res){
  res.send('<h1>Hello world</h1>');
});

io.on('connection', function(socket) {
	socket.on('game', function(msg) {
		socket.join(msg);
		socket.broadcast.to(msg).emit('joined', '');
		// console.log(msg);
	});

	socket.on('chat', function(msg) {
		socket.broadcast.to(msg.id).emit('chat', msg.data);
		// console.log(msg);
	});

	socket.on('yes', function(msg) {
		socket.broadcast.to(msg).emit('yes', '');
	});

	socket.on('no', function(msg) {
		socket.broadcast.to(msg).emit('no', '');
	});

	socket.on('done', function(msg) {
		socket.broadcast.to(msg).emit('done', '');
	});

	socket.on('accepted', function(msg) {
		socket.broadcast.to(msg).emit('accepted', '');
	});

	socket.on('stroke', function(msg) {
		// console.log(msg);
		socket.broadcast.to(msg.id).emit('stroke', msg.data);
	});

	socket.on('stroke-start', function(msg) {
		socket.broadcast.to(msg.id).emit('stroke-start', msg.data);
	});

	socket.on('stroke-end', function(msg) {
		socket.broadcast.to(msg).emit('stroke-end', '');
	});

	socket.on('highlight', function(msg) {
		socket.broadcast.to(msg.id).emit('highlight', msg.data);
	});

});

http.listen(3000, function(){
  console.log('listening on *:3000');
});
