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

    function empowerDeletes(scope) {
        $('.poll-delete-answer', scope).click(function () {
            $(this).parent().remove();
        });
    }

    // Above this point are other settings.
    var starting_point = 3;
    function empowerArrows(scope) {
        $('.poll-move-up', scope).click(function () {
            var tag = $(this).parent().parent().parent();
            if (tag.index() <= starting_point){
                return;
            }
            tag.prev().before(tag);
            tag.fadeOut(250).fadeIn(250);
        });
        $('.poll-move-down', scope).click(function () {
            var tag = $(this).parent().parent().parent();
            if ((tag.index() >= (tag.parent().children().length - 1))) {
                return;
            }
            tag.next().after(tag);
            tag.parent().parent().parent().scrollTop(tag.offset().top);
            tag.fadeOut(250).fadeIn(250);
        });
    }

    function displayAnswers(data) {
        pollLineItems.append(answerTemplate(data));
        empowerDeletes(element);
        empowerArrows(element);
    }

    $('#poll-add-answer', element).click(function () {
        pollLineItems.append(answerTemplate({'answers': [{'key': generateUUID(), 'text': ''}]}));
        var new_answer = $(pollLineItems.children().last());
        empowerDeletes(new_answer);
        empowerArrows(new_answer);
        new_answer.fadeOut(250).fadeIn(250);
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
            if (this.name.indexOf('answer-') == 0){
                poll_order.push(this.name);
            }
        });
        data['title'] = $('#poll-title', element).val();
        data['question'] = $('#poll-question-editor', element).val();
        data['feedback'] = $('#poll-feedback-editor', element).val();
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