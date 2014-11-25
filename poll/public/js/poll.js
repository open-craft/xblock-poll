/* Javascript for PollBlock. */
function PollBlock(runtime, element) {

    var voteUrl = runtime.handlerUrl(element, 'vote');
    var tallyURL = runtime.handlerUrl(element, 'get_results');

    var submit = $('input[type=button]', element);
    var resultsTemplate = Handlebars.compile($("#results", element).html());
    function getResults(data) {
        if (! data['success']) {
            alert(data['errors'].join('\n'));
        }
        $.ajax({
            // Semantically, this would be better as GET, but we can use helper
            // functions with POST.
            type: "POST",
            url: tallyURL,
            data: JSON.stringify({}),
            success: function (data) {
                $('div.poll-block', element).html(resultsTemplate(data));
            }
        })
    }


    function enableSubmit() {
        submit.removeAttr("disabled");
        answers.unbind("change.EnableSubmit");
    }

    // If the submit button doesn't exist, the user has already
    // selected a choice.
    if (submit.length) {
        var radio = $('input[name=choice]:checked', element);
        submit.click(function (event) {
            // Refresh.
            radio = $(radio.selector, element);
            var choice = radio.val();
            $.ajax({
                type: "POST",
                url: voteUrl,
                data: JSON.stringify({"choice": choice}),
                success: getResults
            });
        });
        // If the user has refreshed the page, they may still have an answer
        // selected and the submit button should be enabled.
        var answers = $('input[type=radio]', element);
        if (! radio.val()) {
            answers.bind("change.EnableSubmit", enableSubmit);
        } else {
            enableSubmit();
        }
    } else {
        getResults({'success': true});
    }
}