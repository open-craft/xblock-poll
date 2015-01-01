/* Javascript for PollBlock. */

function PollUtil (runtime, element) {

    this.init = function(runtime, element) {
        this.voteUrl = runtime.handlerUrl(element, 'vote');
        this.tallyURL = runtime.handlerUrl(element, 'get_results');
        this.element = element;
        this.runtime = runtime;
        this.submit = $('input[type=button]', element);
        this.answers = $('input[type=radio]', element);
        this.resultsTemplate = Handlebars.compile($("#poll-results-template", element).html());
    };

    this.pollInit = function(){
        // If the submit button doesn't exist, the user has already
        // selected a choice.
        var self = this;
        var enableSubmit = self.enableSubmit();
        var getResults = self.getResults();
        if (self.submit.length) {
            var radio = $('input[name=choice]:checked', self.element);
            self.submit.click(function () {
                // Refresh.
                radio = $(radio.selector, self.element);
                var choice = radio.val();
                $.ajax({
                    type: "POST",
                    url: self.voteUrl,
                    data: JSON.stringify({"choice": choice}),
                    success: getResults
                });
            });
            // If the user has refreshed the page, they may still have an answer
            // selected and the submit button should be enabled.
            var answers = $('input[type=radio]', self.element);
            if (! radio.val()) {
                answers.bind("change.EnableSubmit", enableSubmit);
            } else {
                enableSubmit();
            }
        } else {
            getResults({'success': true});
        }
    };

    this.surveyInit = function () {

    };

    this.getResults = function () {
        var self = this;
        return function(data) {
            if (!data['success']) {
                alert(data['errors'].join('\n'));
            }
            $.ajax({
                // Semantically, this would be better as GET, but we can use helper
                // functions with POST.
                type: "POST",
                url: self.tallyURL,
                data: JSON.stringify({}),
                success: function (data) {
                    console.log(self);
                    $('div.poll-block', self.element).html(self.resultsTemplate(data));
                }
            })
        }
    };

    this.enableSubmit = function () {
        var self = this;
        return function () {
            self.submit.removeAttr("disabled");
            self.answers.unbind("change.EnableSubmit");
        }
    };
    this.init(runtime, element);
}

function PollBlock(runtime, element) {
    var util = new PollUtil(runtime, element);
    util.pollInit();
}

function SurveyBlock(runtime, element) {
    var util = new PollUtil(runtime, element);
    util.surveyInit();
}
