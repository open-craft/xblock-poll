/* JavaScript utils for both LMS and Studio poll. */

var PollCommonUtil = {
    init: function (Handlebars) {
        // Make gettext available in Handlebars templates
        Handlebars.registerHelper('gettext', function (str) {
            return PollXBlockI18N.gettext(str);
        });

        // Make ngettext available in Handlebars templates
        Handlebars.registerHelper('ngettext', function (singular, plural, count) {
            return PollXBlockI18N.ngettext(singular, plural, count);
        });

        // Add helper for interpolating values into strings in Handlebars templates
        Handlebars.registerHelper('interpolate', function (formatString, parameters) {
            parameters = parameters.hash;
            return formatString.replace(/{\w+}/g,
                function (parameter) {
                    var parameterName = parameter.slice(1, -1);
                    return String(parameters[parameterName]);
                });
        });

        // Add helper for equality check
        Handlebars.registerHelper('if_eq', function (a, b, opts) {
            if(a == b)
                return opts.fn(this);
            else
                return opts.inverse(this);
        });
    }
};
