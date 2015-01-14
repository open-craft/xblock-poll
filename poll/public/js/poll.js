/* Javascript for PollBlock. */

function PollUtil (runtime, element, pollType) {
    var self = this;

    this.init = function() {
        // Initialization function used for both Poll Types
        this.voteUrl = runtime.handlerUrl(element, 'vote');
        this.tallyURL = runtime.handlerUrl(element, 'get_results');
        this.submit = $('input[type=button]', element);
        this.answers = $('input[type=radio]', element);
        this.resultsTemplate = Handlebars.compile($("#" + pollType + "-results-template", element).html());
        // If the submit button doesn't exist, the user has already
        // selected a choice. Render results instead of initializing machinery.
        if (! self.submit.length) {
            self.getResults({'success': true});
            return false;
        }
        return true;
    };

    this.pollInit = function(){
        // Initialization function for PollBlocks.

        var radio = $('input[name=choice]:checked', element);
        self.submit.click(function () {
            // Refresh.
            radio = $(radio.selector, element);
            var choice = radio.val();
            $.ajax({
                type: "POST",
                url: self.voteUrl,
                data: JSON.stringify({"choice": choice}),
                success: self.getResults
            });
        });
        // If the user has refreshed the page, they may still have an answer
        // selected and the submit button should be enabled.
        var answers = $('input[type=radio]', element);
        if (! radio.val()) {
            answers.bind("change.enableSubmit", self.enableSubmit);
        } else {
            self.enableSubmit();
        }
    };

    this.surveyInit = function () {
        // Initialization function for Survey Blocks
        self.answers.bind("change.enableSubmit", self.verifyAll);
        self.submit.click(function () {
            $.ajax({
                type: "POST",
                url: self.voteUrl,
                data: JSON.stringify(self.surveyChoices()),
                success: self.getResults
            })
        });
        // If the user has refreshed the page, they may still have an answer
        // selected and the submit button should be enabled.
        self.verifyAll();
    };

    this.surveyChoices = function () {
        // Grabs all selections for survey answers, and returns a mapping for them.
        var choices = {};
        self.answers.each(function(index, el) {
            el = $(el);
            choices[el.prop('name')] = $(self.checkedElement(el)).val();
        });
        return choices;
    };

    this.checkedElement = function (el) {
        // Given the DOM element of a radio, get the selector for the checked element
        // with the same name.
        return "input[name='" + el.prop('name') + "']:checked"
    };

    this.verifyAll = function () {
        // Verify that all questions have an answer selected.
        var doEnable = true;
        self.answers.each(function (index, el) {
            if (! $(self.checkedElement($(el)), element).length) {
                doEnable = false;
                return false
            }
        });
        if (doEnable){
            self.enableSubmit();
        }
    };

    this.getResults = function (data) {
        // Fetch the results from the server and render them.
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
                $('div.poll-block', element).html(self.resultsTemplate(data));
            }
        })
    };

    this.enableSubmit = function () {
        // Enable the submit button.
        self.submit.removeAttr("disabled");
        self.answers.unbind("change.enableSubmit");
    };

    var run_init = this.init();
    if (run_init) {
        var init_map = {'poll': self.pollInit, 'survey': self.surveyInit};
        init_map[pollType]()
    }

}

function PollBlock(runtime, element) {
    new PollUtil(runtime, element, 'poll');
}

function SurveyBlock(runtime, element) {
    new PollUtil(runtime, element, 'survey');
}
