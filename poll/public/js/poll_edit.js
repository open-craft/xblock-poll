
function PollEditUtil(runtime, element, pollType) {
    var self = this;

    this.init = function () {
        // Set up the editing form for a Poll or Survey.
        self.loadAnswers = runtime.handlerUrl(element, 'load_answers');
        var temp = $('#answer-form-component', element).html();
        self.answerTemplate = Handlebars.compile(temp);

        $(element).find('.cancel-button', element).bind('click', function() {
            runtime.notify('cancel', {});
        });
        var mapping = self.mappings[pollType]['buttons'];
        for (var key in mapping) {
            if (mapping.hasOwnProperty(key)) {
                $(key, element).click(
                    // The nature of the closure forces us to make a custom function here.
                    function (context_key, topMarker, bottomMarker) {
                        return function () {
                            // The degree of precision on date should be precise enough to avoid
                            // collisions in the real world.
                            var bottom = $(bottomMarker);
                            $(self.answerTemplate(mapping[context_key]['itemList'])).before(bottom);
                            var new_item = bottom.prev();
                            self.empowerDeletes(new_item);
                            self.empowerArrows(
                                new_item, mapping[context_key]['topMarker'],
                                mapping[context_key]['bottomMarker']
                            );
                            new_item.fadeOut(250).fadeIn(250);
                        }
                    }(key, self.mappings[pollType])
                )
            }
        }

        $(element).find('.save-button', element).bind('click', self.pollSubmitHandler);

        $(function ($) {
            $.ajax({
                type: "POST",
                url: self.loadAnswers,
                data: JSON.stringify({}),
                success: self.displayAnswers
            });
        });
    };

    this.extend = function (obj1, obj2) {
        // Mimics similar extend functions, making obj1 contain obj2's properties.
        for (var attrname in obj2) {
            if (obj2.hasOwnProperty(attrname)) {
                obj1[attrname] = obj2[attrname]
            }
        }
        return obj1;
    };

    this.makeNew = function(extra){
        // Make a new empty line item, like a question or an answer.
        // 'extra' should contain 'image', a boolean value that determines whether
        // an image path field should be provided, and 'noun', which should be either
        // 'question' or 'answer' depending on what is needed.
        return self.extend({'key': new Date().getTime(), 'text': '', 'img': ''}, extra)
    };

    // This object is used to swap out values which differ between Survey and Poll blocks.
    this.mappings = {
        'poll': {
            'buttons': {
                '#poll-add-answer': {
                    'itemList': {'items': [self.makeNew({'image': true, 'noun': 'answer'})]},
                    'topMarker': '#poll-answer-marker', 'bottomMarker': '#poll-answer-end-marker'
                }
            },
            'onLoad': {

            }
        },
        'survey': {
            'buttons': {
                '#poll-add-answer': {
                    'itemList': {'items': [self.makeNew({'image': false, 'noun': 'answer'})]},
                    'topMarker': '#poll-answer-marker', 'bottomMarker': '#poll-answer-end-marker'
                },
                '#poll-add-question': {
                    'itemList': {'items': [self.makeNew({'image': true, 'noun': 'question'})]}
                }
            }
        }
    };

    this.empowerDeletes = function (scope) {
        // Activates the delete buttons on rendered line items.
        $('.poll-delete-answer', scope).click(function () {
            $(this).parent().remove();
        });
    };

    this.empowerArrows = function(scope, topMarker, bottomMarker) {
        // Activates the arrows on rendered line items.
        $('.poll-move-up', scope).click(function () {
            var tag = $(this).parents('li');
            if (tag.index() <= ($(topMarker).index() + 1)){
                return;
            }
            tag.prev().before(tag);
            tag.fadeOut("fast", "swing").fadeIn("fast", "swing");
        });
        $('.poll-move-down', scope).click(function () {
            var tag = $(this).parents('li');
            if ((tag.index() >= ($(bottomMarker).index() - 1))) {
                return;
            }
            tag.next().after(tag);
            tag.fadeOut("fast", "swing").fadeIn("fast", "swing");
        });
    };

    this.displayAnswers = function (data){
        self.displayItems(data, '#poll-answer-marker', '#poll-answer-end-marker')
    };

    this.displayItems = function(data, topMarker, bottomMarker) {
        // Loads the initial set of items that the block needs to edit.
        $('#poll-answer-end-marker').before(self.answerTemplate(data));
        self.empowerDeletes(element, topMarker, bottomMarker);
        self.empowerArrows(element, topMarker, bottomMarker);
    };

    this.check_return = function(data) {
        // Handle the return value JSON from the server.
        // It would be better if we could have a different function
        // for errors, as AJAX calls normally allow, but our version of XBlock
        // does not support status codes other than 200 for JSON encoded
        // responses.
        if (data['success']) {
            window.location.reload(false);
            return;
        }
        alert(data['errors'].join('\n'));
    };

    this.pollSubmitHandler = function() {
        // Take all of the fields, serialize them, and pass them to the
        // server for saving.
        var handlerUrl = runtime.handlerUrl(element, 'studio_submit');
        var data = {'answers': []};
        var tracker = [];
        $('#poll-form input', element).each(function() {
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

        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify(data),
            success: self.check_return
        });
    };

    self.init();
}

function PollEdit(runtime, element) {
    new PollEditUtil(runtime, element, 'poll');
}

function SurveyEdit(runtime, element) {
    new PollEditUtil(runtime, element, 'survey');
}
