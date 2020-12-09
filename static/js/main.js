(function(){

    const socket = io('http://localhost:5000');
    const $receive_data = $('#receive-data');

    socket.on('receive_data', function(data) {
        $receive_data.val(data + $receive_data.val());

        if (data == 'Serial port is opened\n') 
            $('#cmd-port').text('Close Port').removeClass('btn-success').addClass('btn-danger');
        else if (data == 'Serial port is closed\n')
            $('#cmd-port').text('Open Port').removeClass('btn-danger').addClass('btn-success');
    });

    $('#cmd-port').on('click', function (evt) {
        var cmd = $(this).text();

        if (cmd == 'Open Port')
            socket.emit('open_port', {port: $('#port').val(), baudrate: $('#baudrate').val()});
        else
            socket.emit('close_port', 'Close Port');
    });

    $('#send-message').on('click', function (evt) {
        socket.emit('send_message', $('#message').val() + '\n');
    });

    $('#message').on('keydown', function (evt) {
        if (evt.keyCode == 13) {
            $('#send-message').trigger('click');
            return false;
        }  
    });

    $('#clear').on('click', function (evt) {
        $('#receive-data').val('');
    });

})();