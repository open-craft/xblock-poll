
            (function(global){
                var PollXBlockI18N = {
                  init: function() {
                    

(function(globals) {

  var django = globals.django || (globals.django = {});

  
  django.pluralidx = function(count) { return (count == 1) ? 0 : 1; };
  

  /* gettext library */

  django.catalog = django.catalog || {};
  
  var newcatalog = {
    "Answer": "\u0625\u062c\u0627\u0628\u0629", 
    "Delete": "\u062d\u0630\u0641", 
    "Feedback": "\u0627\u0644\u062a\u0639\u0644\u064a\u0642\u0627\u062a", 
    "Image URL": "\u0639\u0646\u0648\u0627\u0646 URL \u0644\u0635\u0648\u0631\u0629", 
    "Image alternative text": "\u0627\u0644\u0646\u0635 \u0627\u0644\u0628\u062f\u064a\u0644 \u0644\u0644\u0635\u0648\u0631\u0629", 
    "Question": "\u0633\u0624\u0627\u0644", 
    "Results": "\u0627\u0644\u0646\u062a\u0627\u0626\u062c", 
    "Results gathered from {total} respondent.": [
      "\u0627\u0644\u0646\u062a\u0627\u0626\u062c \u0627\u0644\u0645\u062c\u0645\u0639\u0629 \u0645\u0646 {total} \u0645\u0646 \u0627\u0644\u0645\u0633\u062a\u062c\u064a\u0628\u064a\u0646.", 
      "\u0627\u0644\u0646\u062a\u0627\u0626\u062c \u0627\u0644\u0645\u062c\u0645\u0639\u0629 \u0645\u0646 {total} \u0645\u0646 \u0627\u0644\u0645\u0633\u062a\u062c\u064a\u0628\u064a\u0646."
    ], 
    "Submit": "\u062a\u0642\u062f\u064a\u0645", 
    "This must have an image URL or text, and can have both.  If you add an image, you must also provide an alternative text that describes the image in a way that would allow someone to answer the poll if the image did not load.": "\u064a\u062c\u0628 \u0623\u0646 \u064a\u062d\u062a\u0648\u064a \u0647\u0630\u0627 \u0639\u0644\u0649 \u0639\u0646\u0648\u0627\u0646 URL \u0644\u0635\u0648\u0631\u0629 \u0623\u0648 \u0646\u0635\u060c \u0648\u0642\u062f \u064a\u062d\u062a\u0648\u064a \u0639\u0644\u0649 \u0643\u0644\u064a\u0647\u0645\u0627. \u0625\u0630\u0627 \u0623\u0636\u0641\u062a \u0635\u0648\u0631\u0629\u060c \u0641\u064a\u062c\u0628 \u0623\u0646 \u062a\u0648\u0641\u0631 \u0646\u0635\u0627\u064b \u0628\u062f\u064a\u0644\u0627\u064b \u0623\u064a\u0636\u0627\u064b \u064a\u0634\u0631\u062d \u0627\u0644\u0635\u0648\u0631\u0629 \u0628\u0637\u0631\u064a\u0642\u0629 \u062a\u0645\u0643\u0646 \u0623\u064a \u0634\u062e\u0635 \u0645\u0646 \u0627\u0644\u0625\u062c\u0627\u0628\u0629 \u0639\u0644\u0649 \u0627\u0644\u0627\u0633\u062a\u0637\u0644\u0627\u0639 \u0641\u064a \u062d\u0627\u0644 \u0639\u062f\u0645 \u062a\u062d\u0645\u064a\u0644 \u0627\u0644\u0635\u0648\u0631\u0629.", 
    "You can make limited use of Markdown in answer texts, preferably only bold and italics.": "\u064a\u0645\u0643\u0646\u0643 \u0627\u0633\u062a\u062e\u062f\u0627\u0645 Markdown \u0628\u0634\u0643\u0644 \u0645\u062d\u062f\u0648\u062f \u0641\u064a \u0646\u0635\u0648\u0635 \u0627\u0644\u0625\u062c\u0627\u0628\u0629\u060c \u0648\u064a\u0641\u0636\u0644 \u0628\u0627\u0644\u062e\u0637 \u0627\u0644\u0639\u0631\u064a\u0636 \u0648\u0627\u0644\u0645\u0627\u0626\u0644 \u0641\u0642\u0637.", 
    "move poll down": "\u062a\u062d\u0631\u064a\u0643 \u0627\u0633\u062a\u0637\u0644\u0627\u0639 \u0627\u0644\u0631\u0623\u064a \u0644\u0644\u0623\u0633\u0641\u0644", 
    "move poll up": "\u062a\u062d\u0631\u064a\u0643 \u0627\u0633\u062a\u0637\u0644\u0627\u0639 \u0627\u0644\u0631\u0623\u064a \u0644\u0644\u0623\u0639\u0644\u0649"
  };
  for (var key in newcatalog) {
    django.catalog[key] = newcatalog[key];
  }
  

  if (!django.jsi18n_initialized) {
    django.gettext = function(msgid) {
      var value = django.catalog[msgid];
      if (typeof(value) == 'undefined') {
        return msgid;
      } else {
        return (typeof(value) == 'string') ? value : value[0];
      }
    };

    django.ngettext = function(singular, plural, count) {
      var value = django.catalog[singular];
      if (typeof(value) == 'undefined') {
        return (count == 1) ? singular : plural;
      } else {
        return value[django.pluralidx(count)];
      }
    };

    django.gettext_noop = function(msgid) { return msgid; };

    django.pgettext = function(context, msgid) {
      var value = django.gettext(context + '\x04' + msgid);
      if (value.indexOf('\x04') != -1) {
        value = msgid;
      }
      return value;
    };

    django.npgettext = function(context, singular, plural, count) {
      var value = django.ngettext(context + '\x04' + singular, context + '\x04' + plural, count);
      if (value.indexOf('\x04') != -1) {
        value = django.ngettext(singular, plural, count);
      }
      return value;
    };

    django.interpolate = function(fmt, obj, named) {
      if (named) {
        return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
      } else {
        return fmt.replace(/%s/g, function(match){return String(obj.shift())});
      }
    };


    /* formatting library */

    django.formats = {
    "DATETIME_FORMAT": "N j, Y, P", 
    "DATETIME_INPUT_FORMATS": [
      "%Y-%m-%d %H:%M:%S", 
      "%Y-%m-%d %H:%M:%S.%f", 
      "%Y-%m-%d %H:%M", 
      "%Y-%m-%d", 
      "%m/%d/%Y %H:%M:%S", 
      "%m/%d/%Y %H:%M:%S.%f", 
      "%m/%d/%Y %H:%M", 
      "%m/%d/%Y", 
      "%m/%d/%y %H:%M:%S", 
      "%m/%d/%y %H:%M:%S.%f", 
      "%m/%d/%y %H:%M", 
      "%m/%d/%y"
    ], 
    "DATE_FORMAT": "j F\u060c Y", 
    "DATE_INPUT_FORMATS": [
      "%Y-%m-%d", 
      "%m/%d/%Y", 
      "%m/%d/%y", 
      "%b %d %Y", 
      "%b %d, %Y", 
      "%d %b %Y", 
      "%d %b, %Y", 
      "%B %d %Y", 
      "%B %d, %Y", 
      "%d %B %Y", 
      "%d %B, %Y"
    ], 
    "DECIMAL_SEPARATOR": ",", 
    "FIRST_DAY_OF_WEEK": "0", 
    "MONTH_DAY_FORMAT": "j F", 
    "NUMBER_GROUPING": "0", 
    "SHORT_DATETIME_FORMAT": "m/d/Y P", 
    "SHORT_DATE_FORMAT": "d\u200f/m\u200f/Y", 
    "THOUSAND_SEPARATOR": ".", 
    "TIME_FORMAT": "g:i A", 
    "TIME_INPUT_FORMATS": [
      "%H:%M:%S", 
      "%H:%M:%S.%f", 
      "%H:%M"
    ], 
    "YEAR_MONTH_FORMAT": "F Y"
  };

    django.get_format = function(format_type) {
      var value = django.formats[format_type];
      if (typeof(value) == 'undefined') {
        return format_type;
      } else {
        return value;
      }
    };

    /* add to global namespace */
    globals.pluralidx = django.pluralidx;
    globals.gettext = django.gettext;
    globals.ngettext = django.ngettext;
    globals.gettext_noop = django.gettext_noop;
    globals.pgettext = django.pgettext;
    globals.npgettext = django.npgettext;
    globals.interpolate = django.interpolate;
    globals.get_format = django.get_format;

    django.jsi18n_initialized = true;
  }

}(this));


                  }
                };
                PollXBlockI18N.init();
                global.PollXBlockI18N = PollXBlockI18N;
            }(this));
        