function PollEditBlock(runtime, element) {
    var loadAnswers = runtime.handlerUrl(element, 'load_answers');
    var temp = $('#answer-form-component', element).html();
    var answerTemplate = Handlebars.compile(temp);
    var pollLineItems =$('#poll-line-items', element);

    function empowerDeletes(scope) {
        $('.poll-delete-answer', scope).click(function () {
            $(this).parent().remove();
        });
    }

    /*
    The poll answers need to be reorderable. As the UL they are in is not
    easily isolated, we need to start checking their position to make
    sure they aren't ordered above the other settings, which are also
    in the list.
    */
    var starting_point = 3;
    function empowerArrows(scope) {
        $('.poll-move-up', scope).click(function () {
            var tag = $(this).parents('li');
            if (tag.index() <= starting_point){
                return;
            }
            tag.prev().before(tag);
            tag.fadeOut("fast", "swing").fadeIn("fast", "swing");
        });
        $('.poll-move-down', scope).click(function () {
            var tag = $(this).parents('li');
            if ((tag.index() >= (tag.parent().children().length - 1))) {
                return;
            }
            tag.next().after(tag);
            tag.fadeOut("fast", "swing").fadeIn("fast", "swing");
        });
    }

    function displayAnswers(data) {
        pollLineItems.append(answerTemplate(data));
        empowerDeletes(element);
        empowerArrows(element);
    }

    $('#poll-add-answer', element).click(function () {
        // The degree of precision on date should be precise enough to avoid
        // collisions in the real world.
        pollLineItems.append(answerTemplate({'answers': [{'key': new Date().getTime(), 'text': ''}]}));
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
        var data = {'answers': []};
        var tracker = [];
        $('#poll-form input', element).each(function(i) {
            var key = 'label';
            if (this.name.indexOf('answer-') >= 0){
                var name = this.name.replace('answer-', '');
                if (this.name.indexOf('img-') == 0){
                    name = name.replace('img-', '');
                    key = 'img'
                }
                if (tracker.indexOf(name) == -1){
                    tracker.push(name);
                    data['answers'].push({'key': name})
                }
                var index = tracker.indexOf(name);
                data['answers'][index][key] = this.value;
                return
            }
            data[this.name] = this.value
        });
        data['title'] = $('#poll-title', element).val();
        data['question'] = $('#poll-question-editor', element).val();
        data['feedback'] = $('#poll-feedback-editor', element).val();
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