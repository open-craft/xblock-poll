function PollEditUtil(runtime, element, pollType) {
    var self = this;
    var notify;

    // These URLs aren't validated in real time, so even if they don't exist for a type of block
    // we can create a reference to them.
    this.loadAnswers = runtime.handlerUrl(element, 'load_answers');
    this.loadQuestions = runtime.handlerUrl(element, 'load_questions');

    // The workbench doesn't support notifications.
    notify = typeof(runtime.notify) != 'undefined';

    this.init = function () {
        // Set up the editing form for a Poll or Survey.
        var temp = $('.poll-form-component', element).html();

        // Set up gettext in case it isn't available in the client runtime:
        if (typeof gettext == "undefined") {
            window.gettext = function gettext_stub(string) { return string; };
            window.ngettext = function ngettext_stub(strA, strB, n) { return n == 1 ? strA : strB; };
        }

        // Make gettext available in Handlebars templates
        Handlebars.registerHelper('i18n', function(str) { return gettext(str); });

        // Make ngettext available in Handlebars templates
        Handlebars.registerHelper('i18n_ngettext', function(singular, plural, count) {
            return ngettext(singular, plural, count);
        });

        // Add helper for interpolating values into strings in Handlebars templates
        Handlebars.registerHelper('interpolate', function(formatString, parameters) {
            parameters = parameters.hash;
            return formatString.replace(/{\w+}/g,
                function(parameter) {
                    var parameterName = parameter.slice(1, -1);
                    return String(parameters[parameterName]);
                });
        });

        self.answerTemplate = Handlebars.compile(temp);

        $(element).find('.cancel-button', element).bind('click', function() {
            runtime.notify('cancel', {});
        });
        var button_mapping = self.mappings[pollType]['buttons'];
        for (var key in button_mapping) {
            if (button_mapping.hasOwnProperty(key)) {
                $(key, element).click(
                    // The nature of the closure forces us to make a custom function here.
                    function (context_key) {
                        return function () {
                            // The degree of precision on date should be precise enough to avoid
                            // collisions in the real world.
                            var bottom = $(button_mapping[context_key]['bottomMarker']);
                            var new_item_dict = self.extend({}, button_mapping[context_key]['template']);
                            // We have to insert this key now rather than keep it in the template
                            // so that it's generated with the current time. If we constructed it as part
                            // of the template, all the keys would be the same, since the time would be calculated
                            // once.
                            new_item_dict['key'] = Date.now();
                            var new_item = $(self.answerTemplate({'items': [new_item_dict]}));
                            bottom.before(new_item);
                            self.empowerDeletes(new_item);
                            self.empowerArrows(
                                new_item, button_mapping[context_key]['topMarker'],
                                button_mapping[context_key]['bottomMarker']
                            );
                            self.scrollTo(new_item);
                            new_item.fadeOut(0).fadeIn('slow', 'swing');
                        }
                    }(key)
                )
            }
        }

        $(element).find('.save-button', element).bind('click', self.pollSubmitHandler);

        var mapping = self.mappings[pollType]['onLoad'];
        for (var task in mapping) {
            function load (taskItem){
                $(function ($) {
                    $.ajax({
                        type: "POST",
                        url: taskItem['url'],
                        data: JSON.stringify({}),
                        success: taskItem['function']
                    });
                });
            }
            load(mapping[task]);
        }
    };

    this.scrollTo = function (item){
        // Scrolls to the center of a particular item in the settings, then flash it.
        var parent = $('#poll-line-items');
        var item_center = parent.scrollTop() + item.position().top - parent.height()/2 + item.height() / 2;
        parent.animate({ scrollTop: item_center }, "slow");
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

        // A 'key' element will have to be added after the fact, since it needs to be
        // generated with the current time.
        return self.extend({'text': '', 'img': '', 'img_alt': ''}, extra)
    };

    this.empowerDeletes = function (scope) {
        // Activates the delete buttons on rendered line items.
        $('.poll-delete-answer', scope).click(function () {
            $(this).parent().remove();
        });
    };

    this.empowerArrows = function(scope, topMarker, bottomMarker) {
        // Activates the arrows on rendered line items.
        $('.poll-move-up', scope).click(function (ev) {
            var tag = $(this).parents('li');
            if (tag.index() <= ($(topMarker).index() + 1)){
                return;
            }
            tag.prev().before(tag);
            tag.fadeOut(0).fadeIn('slow', 'swing');
            self.scrollTo(tag);
            ev.preventDefault();
        });
        $('.poll-move-down', scope).click(function () {
            var tag = $(this).parents('li');
            if ((tag.index() >= ($(bottomMarker).index() - 1))) {
                return;
            }
            tag.next().after(tag);
            tag.fadeOut(0).fadeIn('slow', 'swing');
            self.scrollTo(tag);
            ev.preventDefault();
        });
    };

    this.displayAnswers = function (data){
        self.displayItems(data, '#poll-answer-marker', '#poll-answer-end-marker')
    };

    this.displayQuestions = function (data) {
        self.displayItems(data, "#poll-question-marker", '#poll-question-end-marker')
    };

    // This object is used to swap out values which differ between Survey and Poll blocks.
    this.mappings = {
        'poll': {
            'buttons': {
                '#poll-add-answer': {
                    'template': self.makeNew({'image': true, 'noun': 'answer'}),
                    'topMarker': '#poll-answer-marker', 'bottomMarker': '#poll-answer-end-marker'
                }
            },
            'onLoad': [{'url': self.loadAnswers, 'function': self.displayAnswers}],
            'gather': [{'prefix': 'answer', 'field': 'answers'}]
        },
        'survey': {
            'buttons': {
                '#poll-add-answer': {
                    'template': self.makeNew({'image': false, 'noun': 'answer'}),
                    'topMarker': '#poll-answer-marker', 'bottomMarker': '#poll-answer-end-marker'
                },
                '#poll-add-question': {
                    'template': self.makeNew({'image': true, 'noun': 'question'}),
                    'topMarker': '#poll-question-marker', 'bottomMarker': '#poll-question-end-marker'
                }
            },
            'onLoad': [
                {'url': self.loadQuestions, 'function': self.displayQuestions},
                {'url': self.loadAnswers, 'function': self.displayAnswers}
            ],
            'gather': [{'prefix': 'answer', 'field': 'answers'}, {'prefix': 'question', 'field': 'questions'}]
        }
    };

    this.displayItems = function(data, topMarker, bottomMarker) {
        // Loads the initial set of items that the block needs to edit.
        var result = $(self.answerTemplate(data));
        $(bottomMarker).before(result);
        self.empowerDeletes(result, topMarker, bottomMarker);
        self.empowerArrows(result, topMarker, bottomMarker);
    };

    this.gather = function (scope, tracker, data, prefix, field) {
        var key = 'label';
        var name = scope.name.replace(prefix + '-', '');
        if (name.indexOf('img_alt-') == 0) {
            name = name.replace('img_alt-', '');
            key = 'img_alt'
        } else if (name.indexOf('img-') == 0) {
            name = name.replace('img-', '');
            key = 'img'
        } else if (name.indexOf('label-') == 0) {
            name = name.replace('label-', '');
        }
        if (! (scope.name.indexOf(prefix + '-') >= 0)) {
            return
        }
        if (tracker.indexOf(name) == -1) {
            tracker.push(name);
            data[field].push({'key': name})
        }
        var index = tracker.indexOf(name);
        data[field][index][key] = scope.value;
        return true
    };

    this.format_errors = function(errors) {
        var new_list = [];
        for (var line in errors) {
            // Javascript has no sane HTML escape method.
            // Do this instead.
            new_list.push($('<div/>').text(errors[line]).html())
        }
        return new_list.join('<br />')
    };

    this.pollSubmitHandler = function () {
        // Take all of the fields, serialize them, and pass them to the
        // server for saving.
        var handlerUrl = runtime.handlerUrl(element, 'studio_submit');
        var data = {};
        var tracker;
        var gatherings = self.mappings[pollType]['gather'];
        for (var gathering in gatherings) {
            tracker = [];
            var field = gatherings[gathering]['field'];
            var prefix = gatherings[gathering]['prefix'];
            data[field] = [];
            $('#poll-form input', element).each(function () {
                self.gather(this, tracker, data, prefix, field)
            });
        }
        data['display_name'] = $('#poll-display-name', element).val();
        data['question'] = $('#poll-question-editor', element).val();
        data['feedback'] = $('#poll-feedback-editor', element).val();
        data['max_submissions'] = $('#poll-max-submissions', element).val();
        // Convert to boolean for transfer.
        data['private_results'] = eval($('#poll-private-results', element).val());

        if (notify) {
            runtime.notify('save', {state: 'start', message: gettext("Saving")});
        }
        $.ajax({
            type: "POST",
            url: handlerUrl,
            data: JSON.stringify(data),
            // There are issues with using proper status codes at the moment.
            // So we pass along a 'success' key for now.
            success: function(result) {
                if (result['success'] && notify) {
                    runtime.notify('save', {state: 'end'})
                } else if (notify) {
                    runtime.notify('error', {
                        'title': 'Error saving poll',
                        'message': self.format_errors(result['errors'])
                    });
                }
            }
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
