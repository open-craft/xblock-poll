
            (function(global){
                var PollXBlockI18N = {
                  init: function() {
                    

(function(globals) {

  var django = globals.django || (globals.django = {});

  
  django.pluralidx = function(n) {
    var v=(n != 1);
    if (typeof(v) == 'boolean') {
      return v ? 1 : 0;
    } else {
      return v;
    }
  };
  

  /* gettext library */

  django.catalog = django.catalog || {};
  
  var newcatalog = {
    "Answer": "\u00c0nsw\u00e9r \u2c60'\u03c3\u044f\u0454\u043c \u03b9\u03c1\u0455\u03c5#",
    "Delete": "D\u00e9l\u00e9t\u00e9 \u2c60'\u03c3\u044f\u0454\u043c \u03b9\u03c1\u0455\u03c5#",
    "Feedback": "F\u00e9\u00e9d\u00df\u00e4\u00e7k \u2c60'\u03c3\u044f\u0454\u043c \u03b9\u03c1\u0455\u03c5\u043c \u2202#",
    "Image URL": "\u00ccm\u00e4g\u00e9 \u00dbRL \u2c60'\u03c3\u044f\u0454\u043c \u03b9\u03c1\u0455\u03c5\u043c \u2202\u03c3\u0142#",
    "Image alternative text": "\u00ccm\u00e4g\u00e9 \u00e4lt\u00e9rn\u00e4t\u00efv\u00e9 t\u00e9xt \u2c60'\u03c3\u044f\u0454\u043c \u03b9\u03c1\u0455\u03c5\u043c \u2202\u03c3\u0142\u03c3\u044f \u0455\u03b9\u0442 \u03b1\u043c\u0454\u0442, \u00a2#",
    "Question": "Q\u00fc\u00e9st\u00ef\u00f6n \u2c60'\u03c3\u044f\u0454\u043c \u03b9\u03c1\u0455\u03c5\u043c \u2202#",
    "Results": "R\u00e9s\u00fclts \u2c60'\u03c3\u044f\u0454\u043c \u03b9\u03c1\u0455\u03c5\u043c #",
    "Results gathered from {total} respondent.": [
      "R\u00e9s\u00fclts g\u00e4th\u00e9r\u00e9d fr\u00f6m {total} r\u00e9sp\u00f6nd\u00e9nt. \u2c60'\u03c3\u044f\u0454\u043c \u03b9\u03c1\u0455\u03c5\u043c \u2202\u03c3\u0142\u03c3\u044f \u0455\u03b9\u0442 \u03b1\u043c\u0454\u0442, \u00a2\u03c3\u03b7\u0455\u0454\u00a2\u0442\u0454\u0442\u03c5#",
      "R\u00e9s\u00fclts g\u00e4th\u00e9r\u00e9d fr\u00f6m {total} r\u00e9sp\u00f6nd\u00e9nts. \u2c60'\u03c3\u044f\u0454\u043c \u03b9\u03c1\u0455\u03c5\u043c \u2202\u03c3\u0142\u03c3\u044f \u0455\u03b9\u0442 \u03b1\u043c\u0454\u0442, \u00a2\u03c3\u03b7\u0455\u0454\u00a2\u0442\u0454\u0442\u03c5\u044f#"
    ],
    "Submit": "S\u00fc\u00dfm\u00eft \u2c60'\u03c3\u044f\u0454\u043c \u03b9\u03c1\u0455\u03c5#",
    "This must have an image URL or text, and can have both.  If you add an image, you must also provide an alternative text that describes the image in a way that would allow someone to answer the poll if the image did not load.": "Th\u00efs m\u00fcst h\u00e4v\u00e9 \u00e4n \u00efm\u00e4g\u00e9 \u00dbRL \u00f6r t\u00e9xt, \u00e4nd \u00e7\u00e4n h\u00e4v\u00e9 \u00df\u00f6th.  \u00ccf \u00fd\u00f6\u00fc \u00e4dd \u00e4n \u00efm\u00e4g\u00e9, \u00fd\u00f6\u00fc m\u00fcst \u00e4ls\u00f6 pr\u00f6v\u00efd\u00e9 \u00e4n \u00e4lt\u00e9rn\u00e4t\u00efv\u00e9 t\u00e9xt th\u00e4t d\u00e9s\u00e7r\u00ef\u00df\u00e9s th\u00e9 \u00efm\u00e4g\u00e9 \u00efn \u00e4 w\u00e4\u00fd th\u00e4t w\u00f6\u00fcld \u00e4ll\u00f6w s\u00f6m\u00e9\u00f6n\u00e9 t\u00f6 \u00e4nsw\u00e9r th\u00e9 p\u00f6ll \u00eff th\u00e9 \u00efm\u00e4g\u00e9 d\u00efd n\u00f6t l\u00f6\u00e4d. \u2c60'\u03c3\u044f\u0454\u043c \u03b9\u03c1\u0455\u03c5\u043c \u2202\u03c3\u0142\u03c3\u044f \u0455\u03b9\u0442 \u03b1\u043c\u0454\u0442, \u00a2\u03c3\u03b7\u0455\u0454\u00a2\u0442\u0454\u0442\u03c5\u044f \u03b1\u2202\u03b9\u03c1\u03b9\u0455\u03b9\u00a2\u03b9\u03b7g \u0454\u0142\u03b9\u0442, \u0455\u0454\u2202 \u2202\u03c3 \u0454\u03b9\u03c5\u0455\u043c\u03c3\u2202 \u0442\u0454\u043c\u03c1\u03c3\u044f \u03b9\u03b7\u00a2\u03b9\u2202\u03b9\u2202\u03c5\u03b7\u0442 \u03c5\u0442 \u0142\u03b1\u0432\u03c3\u044f\u0454 \u0454\u0442 \u2202\u03c3\u0142\u03c3\u044f\u0454 \u043c\u03b1g\u03b7\u03b1 \u03b1\u0142\u03b9q\u03c5\u03b1. \u03c5\u0442 \u0454\u03b7\u03b9\u043c \u03b1\u2202 \u043c\u03b9\u03b7\u03b9\u043c \u03bd\u0454\u03b7\u03b9\u03b1\u043c, q\u03c5\u03b9\u0455 \u03b7\u03c3\u0455\u0442\u044f\u03c5\u2202 \u0454\u03c7\u0454\u044f\u00a2\u03b9\u0442\u03b1\u0442\u03b9\u03c3\u03b7 \u03c5\u0142\u0142\u03b1\u043c\u00a2\u03c3 \u0142\u03b1\u0432\u03c3\u044f\u03b9\u0455 \u03b7\u03b9\u0455\u03b9 \u03c5\u0442 \u03b1\u0142\u03b9q\u03c5\u03b9\u03c1 \u0454\u03c7 \u0454\u03b1 \u00a2\u03c3\u043c\u043c\u03c3\u2202\u03c3 \u00a2\u03c3\u03b7\u0455\u0454q\u03c5\u03b1\u0442. \u2202\u03c5\u03b9\u0455 \u03b1\u03c5\u0442\u0454 \u03b9\u044f\u03c5\u044f\u0454 \u2202\u03c3\u0142\u03c3\u044f \u03b9\u03b7 \u044f\u0454\u03c1\u044f\u0454\u043d\u0454\u03b7\u2202\u0454\u044f\u03b9\u0442 \u03b9\u03b7 \u03bd\u03c3\u0142\u03c5\u03c1\u0442\u03b1\u0442\u0454 \u03bd\u0454\u0142\u03b9\u0442 \u0454\u0455\u0455\u0454 \u00a2\u03b9\u0142\u0142\u03c5\u043c \u2202\u03c3\u0142\u03c3\u044f\u0454 \u0454\u03c5 \u0192\u03c5g\u03b9\u03b1\u0442 #",
    "You can make limited use of Markdown in answer texts, preferably only bold and italics.": "\u00dd\u00f6\u00fc \u00e7\u00e4n m\u00e4k\u00e9 l\u00efm\u00eft\u00e9d \u00fcs\u00e9 \u00f6f M\u00e4rkd\u00f6wn \u00efn \u00e4nsw\u00e9r t\u00e9xts, pr\u00e9f\u00e9r\u00e4\u00dfl\u00fd \u00f6nl\u00fd \u00df\u00f6ld \u00e4nd \u00eft\u00e4l\u00ef\u00e7s. \u2c60'\u03c3\u044f\u0454\u043c \u03b9\u03c1\u0455\u03c5\u043c \u2202\u03c3\u0142\u03c3\u044f \u0455\u03b9\u0442 \u03b1\u043c\u0454\u0442, \u00a2\u03c3\u03b7\u0455\u0454#",
    "move poll down": "m\u00f6v\u00e9 p\u00f6ll d\u00f6wn \u2c60'\u03c3\u044f\u0454\u043c \u03b9\u03c1\u0455\u03c5\u043c \u2202\u03c3\u0142\u03c3\u044f \u0455\u03b9\u0442#",
    "move poll up": "m\u00f6v\u00e9 p\u00f6ll \u00fcp \u2c60'\u03c3\u044f\u0454\u043c \u03b9\u03c1\u0455\u03c5\u043c \u2202\u03c3\u0142\u03c3\u044f \u0455#"
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
        return value.constructor === Array ? value[django.pluralidx(count)] : value;
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
    "DATETIME_FORMAT": "j\\-\\a \\d\\e F Y\\, \\j\\e H:i",
    "DATETIME_INPUT_FORMATS": [
      "%Y-%m-%d %H:%M:%S",
      "%Y-%m-%d %H:%M",
      "%Y-%m-%d",
      "%Y.%m.%d %H:%M:%S",
      "%Y.%m.%d %H:%M",
      "%Y.%m.%d",
      "%d/%m/%Y %H:%M:%S",
      "%d/%m/%Y %H:%M",
      "%d/%m/%Y",
      "%y-%m-%d %H:%M:%S",
      "%y-%m-%d %H:%M",
      "%y-%m-%d",
      "%Y-%m-%d %H:%M:%S.%f"
    ],
    "DATE_FORMAT": "j\\-\\a \\d\\e F Y",
    "DATE_INPUT_FORMATS": [
      "%Y-%m-%d",
      "%y-%m-%d",
      "%Y %m %d",
      "%d-a de %b %Y",
      "%d %b %Y",
      "%d-a de %B %Y",
      "%d %B %Y",
      "%d %m %Y"
    ],
    "DECIMAL_SEPARATOR": ",",
    "FIRST_DAY_OF_WEEK": 1,
    "MONTH_DAY_FORMAT": "j\\-\\a \\d\\e F",
    "NUMBER_GROUPING": 3,
    "SHORT_DATETIME_FORMAT": "Y-m-d H:i",
    "SHORT_DATE_FORMAT": "Y-m-d",
    "THOUSAND_SEPARATOR": "\u00a0",
    "TIME_FORMAT": "H:i",
    "TIME_INPUT_FORMATS": [
      "%H:%M:%S",
      "%H:%M",
      "%H:%M:%S.%f"
    ],
    "YEAR_MONTH_FORMAT": "F \\d\\e Y"
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
        