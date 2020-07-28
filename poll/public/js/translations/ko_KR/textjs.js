
            (function(global){
                var PollXBlockI18N = {
                  init: function() {
                    

(function(globals) {

  var django = globals.django || (globals.django = {});

  
  django.pluralidx = function(count) { return (count == 1) ? 0 : 1; };
  

  /* gettext library */

  django.catalog = django.catalog || {};
  
  var newcatalog = {
    "Answer": "\ub2f5\ubcc0",
    "Delete": "\uc0ad\uc81c",
    "Feedback": "\ud53c\ub4dc\ubc31",
    "Image URL": "\uc774\ubbf8\uc9c0 URL",
    "Image alternative text": "\uc774\ubbf8\uc9c0 \ub300\uccb4 \ud14d\uc2a4\ud2b8",
    "Question": "\uc9c8\ubb38",
    "Results": "\uacb0\uacfc",
    "Results gathered from {total} respondent.": [
      "\ucd1d {total}\uba85\uc758 \uc751\ub2f5\uc790\ub85c\ubd80\ud130 \uc218\uc9d1\ud55c \uacb0\uacfc\uc785\ub2c8\ub2e4.",
      "\ucd1d {total}\uba85\uc758 \uc751\ub2f5\uc790\ub85c\ubd80\ud130 \uc218\uc9d1\ud55c \uacb0\uacfc\uc785\ub2c8\ub2e4."
    ],
    "Submit": "\uc81c\ucd9c\ud558\uae30",
    "This must have an image URL or text, and can have both.  If you add an image, you must also provide an alternative text that describes the image in a way that would allow someone to answer the poll if the image did not load.": "\uc774\ubbf8\uc9c0 URL \ub610\ub294 \ud14d\uc2a4\ud2b8 \uc911 \ud558\ub098\ub294 \uc788\uc5b4\uc57c \ud558\uba70 \ub458 \ub2e4 \uc788\uc5b4\ub3c4 \ub429\ub2c8\ub2e4. \uc774\ubbf8\uc9c0\ub97c \ucd94\uac00\ud558\ub294 \uacbd\uc6b0, \uc774\ubbf8\uc9c0\uac00 \ub85c\ub4dc\ub418\uc9c0 \uc54a\ub354\ub77c\ub3c4 \ub204\uad6c\ub4e0\uc9c0 \ud22c\ud45c\uc5d0 \ucc38\uc5ec\ud560 \uc218 \uc788\ub3c4\ub85d \uc774\ubbf8\uc9c0\ub97c \uc124\uba85\ud558\ub294 \ub300\uccb4 \ud14d\uc2a4\ud2b8\ub3c4 \uc81c\uacf5\ud574\uc57c \ud569\ub2c8\ub2e4.",
    "You can make limited use of Markdown in answer texts, preferably only bold and italics.": "Markdown\uc740 \ub2f5\ubcc0 \ud14d\uc2a4\ud2b8\uc5d0\uc11c \uc81c\ud55c\uc801\uc73c\ub85c \uc0ac\uc6a9\ud560 \uc218 \uc788\uc73c\uba70 \ubcfc\ub4dc\uccb4 \ubc0f \uc774\ud0e4\ub9ad\uccb4\ub9cc \uc0ac\uc6a9\ud558\ub294 \uac83\uc774 \uc88b\uc2b5\ub2c8\ub2e4.",
    "move poll down": "\ud22c\ud45c \ub0b4\ub9ac\uae30",
    "move poll up": "\ud22c\ud45c \uc62c\ub9ac\uae30"
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
    "DATETIME_FORMAT": "Y\ub144 n\uc6d4 j\uc77c g:i A",
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
      "%m/%d/%y",
      "%Y\ub144 %m\uc6d4 %d\uc77c %H\uc2dc %M\ubd84 %S\ucd08",
      "%Y\ub144 %m\uc6d4 %d\uc77c %H\uc2dc %M\ubd84"
    ],
    "DATE_FORMAT": "Y\ub144 n\uc6d4 j\uc77c",
    "DATE_INPUT_FORMATS": [
      "%Y-%m-%d",
      "%m/%d/%Y",
      "%m/%d/%y",
      "%Y\ub144 %m\uc6d4 %d\uc77c"
    ],
    "DECIMAL_SEPARATOR": ".",
    "FIRST_DAY_OF_WEEK": "0",
    "MONTH_DAY_FORMAT": "n\uc6d4 j\uc77c",
    "NUMBER_GROUPING": "3",
    "SHORT_DATETIME_FORMAT": "Y-n-j H:i",
    "SHORT_DATE_FORMAT": "Y-n-j.",
    "THOUSAND_SEPARATOR": ",",
    "TIME_FORMAT": "A g:i",
    "TIME_INPUT_FORMATS": [
      "%H:%M:%S",
      "%H:%M:%S.%f",
      "%H:%M",
      "%H\uc2dc %M\ubd84 %S\ucd08",
      "%H\uc2dc %M\ubd84"
    ],
    "YEAR_MONTH_FORMAT": "Y\ub144 n\uc6d4"
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
        