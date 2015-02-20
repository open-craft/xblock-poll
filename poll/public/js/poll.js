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
        this.viewResultsButton = $('.view-results-button', element);
        this.viewResultsButton.click(this.getResults);
        // If the submit button doesn't exist, the user has already
        // selected a choice. Render results instead of initializing machinery.
        if (! self.submit.length) {
            self.onSubmit({'success': true});
            return false;
        }
        var max_submissions = parseInt($('.poll-max-submissions', element).text());
        var current_count = parseInt($('.poll-current-count', element).text());
        if (max_submissions > 1 && current_count > 0) {
            $('.poll-submissions-count', element).show();
        }
        return true;
    };

    this.pollInit = function(){
        // Initialization function for PollBlocks.
        var selector = 'input[name=choice]:checked';
        var radio = $(selector, element);
        self.submit.click(function () {
            // We can't just use radio.selector here because the selector
            // is mangled if this is the first time this XBlock is added in
            // studio.
            radio = $(selector, element);
            var choice = radio.val();
            var thanks = $('.poll-voting-thanks', element);
            thanks.addClass('poll-hidden');
            // JQuery's fade functions set element-level styles. Clear these.
            thanks.removeAttr('style');
            $.ajax({
                type: "POST",
                url: self.voteUrl,
                data: JSON.stringify({"choice": choice}),
                success: self.onSubmit
            });
        });
        // If the user has already reached their maximum submissions, all inputs should be disabled.
        if (!$('div.poll-block', element).data('can-vote')) {
            $('input', element).attr('disabled', true);
        }
        // If the user has refreshed the page, they may still have an answer
        // selected and the submit button should be enabled.
        var answers = $('input[type=radio]', element);
        if (! radio.val()) {
            answers.bind("change.enableSubmit", self.enableSubmit);
        } else if ($('div.poll-block', element).data('can-vote')) {
            self.enableSubmit();
        }
    };

    this.surveyInit = function () {
        // Initialization function for Survey Blocks

        // If the user is unable to vote, disable input.
        if (! $('div.poll-block', element).data('can-vote')) {
            $('input', element).attr('disabled', true);
            return
        }
        self.answers.bind("change.enableSubmit", self.verifyAll);
        self.submit.click(function () {
            $.ajax({
                type: "POST",
                url: self.voteUrl,
                data: JSON.stringify(self.surveyChoices()),
                success: self.onSubmit
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
            choices[el.prop('name')] = $(self.checkedElement(el), element).val();
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

    this.onSubmit = function (data) {
        // Fetch the results from the server and render them.
        if (!data['success']) {
            alert(data['errors'].join('\n'));
        }
        var can_vote = data['can_vote'];
        $('.poll-current-count', element).text(data['submissions_count']);
        if (data['max_submissions'] > 1) {
            $('.poll-submissions-count', element).show();
        }
        if ($('div.poll-block', element).data('private')) {
            // User may be changing their vote. Give visual feedback that it was accepted.
            var thanks = $('.poll-voting-thanks', element);
            thanks.removeClass('poll-hidden');
            thanks.fadeOut(0).fadeIn('slow', 'swing');
            $('.poll-feedback-container', element).removeClass('poll-hidden');
            if (can_vote) {
                $('input[name="poll-submit"]', element).val('Resubmit');
            } else {
                $('input', element).attr('disabled', true)
            }
            return;
        }
        // Used if results are not private, to show the user how other students voted.
        self.getResults();
    };

    this.getResults = function () {
        // Used if results are not private, to show the user how other students voted.
        $.ajax({
            // Semantically, this would be better as GET, but we can use helper
            // functions with POST.
            type: "POST",
            url: self.tallyURL,
            data: JSON.stringify({}),
            success: function (data) {
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
