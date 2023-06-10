$(document).ready(function() {
    $('#send-button').click(function() {
        var userInput = $('#user-input').val().trim();
        if (userInput !== '') {
            sendMessage(userInput);
            $('#user-input').val('');
        }
    });

    $('#user-input').keypress(function(event) {
        if (event.which === 13) {
            var userInput = $('#user-input').val().trim();
            if (userInput !== '') {
                sendMessage(userInput);
                $('#user-input').val('');
            }
        }
    });

    function sendMessage(message) {
        var messageContainer = $('<div class="message"></div>');
        var contentElement = $('<div class="content"></div>').text(message);
        messageContainer.append(contentElement);
      
        // Check if the message is from the user or the chatbot
        if (messageContainer.prev().hasClass('user')) {
          messageContainer.addClass('user');
        } else {
          messageContainer.addClass('bot');
        }
      
        $('.chat-messages').append(messageContainer);
        scrollToBottom();
        getChatBotResponse(message);
      }
      

    function getChatBotResponse(userInput) {
        setTimeout( function() {
            $.ajax({
                url: '/get_response',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ 'user_input': userInput }),
                success: function(response) {
                    var messageContainer = $('<div class="message"></div>');
                    var userElement = $('<div class="user"></div>');
                    var contentElement = $('<div class="content"></div>').text(response.response);
                    messageContainer.append(userElement);
                    messageContainer.append(contentElement);
                    $('.chat-messages').append(messageContainer);
                    scrollToBottom();
                }
            });
        }, 2000);
    }

    function scrollToBottom() {
        var chatMessages = document.getElementById('chat-messages');
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});