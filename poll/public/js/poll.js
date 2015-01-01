/* Javascript for PollBlock. */

var PollUtil = {

    init: function(runtime, element) {
        this.voteUrl = runtime.handlerUrl(element, 'vote');
        this.tallyURL = runtime.handlerUrl(element, 'get_results');
        this.element = element;
        this.runtime = runtime;
        this.submit = $('input[type=button]', element);
        this.resultsTemplate = Handlebars.compile($("#poll-results-template", element).html());
    },

    poll_init: function(){
        // If the submit button doesn't exist, the user has already
        // selected a choice.
        var self = this;
        if (self.submit.length) {
            var radio = $('input[name=choice]:checked', self.element);
            self.submit.click(function (event) {
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
            var answers = $('input[type=radio]', self.element);
            if (! radio.val()) {
                answers.bind("change.EnableSubmit", self.enableSubmit);
            } else {
                self.enableSubmit();
            }
        } else {
            self.getResults({'success': true});
        }
    },

    getResults: function(data) {
        var self = this;
        if (! data['success']) {
            alert(data['errors'].join('\n'));
        }
        $.ajax({
            // Semantically, this would be better as GET, but we can use helper
            // functions with POST.
            type: "POST",
            url: self.tallyURL,
            data: JSON.stringify({}),
            success: function (data) {
                $('div.poll-block', self.element).html(self.resultsTemplate(data));
            }
        })
    },

    enableSubmit: function () {
        this.submit.removeAttr("disabled");
        this.answers.unbind("change.EnableSubmit");
    }
};

function PollBlock(runtime, element) {
    PollUtil.init(runtime, element);
    PollUtil.poll_init();
}
