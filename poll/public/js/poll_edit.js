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

    var to_disable = ['#poll-add-answer-link', 'input[type=submit', '.poll-delete-answer'];
    for (var selector in to_disable) {
        $(selector, element).click(function(event) {
                event.preventDefault();
            }
        )
    }

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