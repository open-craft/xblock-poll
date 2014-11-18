function PollEditBlock(runtime, element) {
    var loadAnswers = runtime.handlerUrl(element, 'load_answers');
    var temp = $('#answer-form-component', element).html();
    var answerTemplate = Handlebars.compile(temp);
    var pollLineItems =$('#poll-line-items', element);

    // We probably don't need something this complex, but UUIDs are the
    // standard.
    function generateUUID(){
        var d = new Date().getTime();
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = (d + Math.random()*16)%16 | 0;
            d = Math.floor(d/16);
            return (c=='x' ? r : (r&0x7|0x8)).toString(16);
        })
    }

    function empowerDeletes() {
        $('.poll-delete-answer', element).click(function () {
            $(this).parent().remove();
        });
    }

    function displayAnswers(data) {
        pollLineItems.append(answerTemplate(data));
        empowerDeletes();
    }

    $('#poll-add-answer', element).click(function () {
        pollLineItems.append(answerTemplate({'answers': [{'key': generateUUID(), 'text': ''}]}));
        empowerDeletes();
        pollLineItems.last().scrollTop();
    });

    $(element).find('.cancel-button', element).bind('click', function() {
        runtime.notify('cancel', {});
    });

    $(element).find('.save-button', element).bind('click', function() {
        var handlerUrl = runtime.handlerUrl(element, 'studio_submit');
        var data = {};
        var poll_order = [];
        $('#poll-form input', element).each(function(i) {
            data[this.name] = this.value;
            if (this.name.indexOf('answer-') >= 0){
                poll_order.push(this.name);
            }
        });
        data['title'] = $('#poll-title', element).val();
        data['question'] = $('#question-editor', element).val();
        data['poll_order'] = poll_order;
        function check_return(data) {
            if (data['success']) {
                window.location.reload(false);
                return;
            }
            alert(data['errors'].join('\n'));
        }
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify(data),
            success: check_return
        });
    });

    $(function ($) {
        $.ajax({
            type: "POST",
            url: loadAnswers,
            data: JSON.stringify({}),
            success: displayAnswers
        });
    });
}