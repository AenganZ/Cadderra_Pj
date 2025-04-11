function sendMessage() {
    var userInput = $('#userInput').val();
    if (userInput.trim() === '') return;

    // 사용자 메시지 표시
    $('#chatMessages').append('<div class="message user">' + userInput + '</div>');
    $('#userInput').val('');

    // AJAX 요청
    $.ajax({
        url: 'get_response/',
        type: 'POST',
        data: {
            'message': userInput,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(response) {
            // 봇 응답 표시
            $('#chatMessages').append('<div class="message bot">' + response.message + '</div>');
            // 스크롤을 최신 메시지로 이동
            $('.chat-messages').scrollTop($('.chat-messages')[0].scrollHeight);
        },
        error: function(xhr, status, error) {
            console.error("Error:", error);
            $('#chatMessages').append('<div class="message bot">죄송합니다. 오류가 발생했습니다.</div>');
        }
    });
}

// Enter 키 입력 처리
$('#userInput').keypress(function(e) {
    if (e.which == 13) {
        sendMessage();
        return false;
    }
});
