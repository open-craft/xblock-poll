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

    if (submit.length) {
        var radios = $('input[name=choice]:checked', element);
        submit.click(function (event) {
            // Refresh.
            radios = $(radios.selector, element);
            var choice = radios.val();
            $.ajax({
                type: "POST",
                url: voteUrl,
                data: JSON.stringify({"choice": choice}),
                success: getResults
            });
        });
        var answers = $('li', element);
        function enableSubmit() {
            submit.removeAttr("disabled");
            answers.unbind("change.EnableSubmit");
        }
        if (! radios.val()) {
            answers.bind("change.EnableSubmit", enableSubmit);
        } else {
            enableSubmit();
        }
    } else {
        getResults({'success': true});
    }

    $(function ($) {

    });
}