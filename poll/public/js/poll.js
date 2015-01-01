/* Javascript for PollBlock. */

function PollUtil (runtime, element, pollType) {
    var self = this;
    this.init = function(runtime, element) {
        // Initialization function used for both Poll Types
        this.voteUrl = runtime.handlerUrl(element, 'vote');
        this.tallyURL = runtime.handlerUrl(element, 'get_results');
        this.element = element;
        this.runtime = runtime;
        this.submit = $('input[type=button]', element);
        this.answers = $('input[type=radio]', element);
        this.resultsTemplate = Handlebars.compile($("#poll-results-template", element).html());
        var getResults = this.getResults();
        // If the submit button doesn't exist, the user has already
        // selected a choice. Render results instead of initializing machinery.
        if (! self.submit.length) {
            getResults({'success': true});
            return false;
        }
        return true;
    };

    this.pollInit = function(){
        var self = this;
        // Initialization function for PollBlocks.
        var enableSubmit = self.enableSubmit();

        var radio = $('input[name=choice]:checked', self.element);
        self.submit.click(function () {
            // Refresh.
            radio = $(radio.selector, self.element);
            var choice = radio.val();
            $.ajax({
                type: "POST",
                url: self.voteUrl,
                data: JSON.stringify({"choice": choice}),
                success: self.getResults()
            });
        });
        // If the user has refreshed the page, they may still have an answer
        // selected and the submit button should be enabled.
        var answers = $('input[type=radio]', self.element);
        if (! radio.val()) {
            answers.bind("change.enableSubmit", enableSubmit);
        } else {
            enableSubmit();
        }
    };

    this.surveyInit = function () {
        var self = this;
        // Initialization function for Survey Blocks
        var verifyAll = self.verifyAll();
        self.answers.bind("change.enableSubmit", verifyAll)
    };

    this.verifyAll = function () {
        // Generates a function that will verify all questions have an answer selected.
        var self = this;
        var enableSubmit = self.enableSubmit();
        return function () {
            var doEnable = true;
            self.answers.each(function (index, el) {
                if (! $("input[name='" + $(el).prop('name') + "']:checked", self.element).length) {
                    doEnable = false;
                    return false
                }
            });
            if (doEnable){
                enableSubmit();
            }
        }
    };

    this.getResults = function () {
        // Generates a function that will grab and display results.
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
        // Generates a function which will enable the submit button.
        var self = this;
        return function () {
            self.submit.removeAttr("disabled");
            self.answers.unbind("change.enableSubmit");
        }
    };
    var run_init = this.init(runtime, element);
    if (run_init) {
        var init_map = {'poll': self.pollInit, 'survey': self.surveyInit};
        init_map[pollType].call(self)
    }
}

function PollBlock(runtime, element) {
    new PollUtil(runtime, element, 'poll');
}

function SurveyBlock(runtime, element) {
    new PollUtil(runtime, element, 'survey');
}
