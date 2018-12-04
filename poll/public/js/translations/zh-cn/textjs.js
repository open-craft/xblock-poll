
            (function(global){
                var PollXBlockI18N = {
                  init: function() {
                    

(function (globals) {

  var django = globals.django || (globals.django = {});

  
  django.pluralidx = function (count) { return (count == 1) ? 0 : 1; };
  

  
  /* gettext library */

  django.catalog = {
    "Answer": "\u7b54\u6848", 
    "Delete": "\u5220\u9664", 
    "Feedback": "\u53cd\u9988", 
    "Image URL": "\u56fe\u50cf URL", 
    "Image alternative text": "\u56fe\u50cf\u66ff\u6362\u6587\u672c", 
    "Question": "\u95ee\u9898", 
    "Results": "\u7ed3\u679c", 
    "Results gathered from {total} respondent.": [
      "\u4ece {total} \u4e2a\u56de\u5e94\u8005\u5904\u6536\u96c6\u7684\u7ed3\u679c\u3002", 
      "\u4ece {total} \u4e2a\u56de\u5e94\u8005\u5904\u6536\u96c6\u7684\u7ed3\u679c\u3002"
    ], 
    "Submit": "\u63d0\u4ea4", 
    "This must have an image URL or text, and can have both.  If you add an image, you must also provide an alternative text that describes the image in a way that would allow someone to answer the poll if the image did not load.": "\u5176\u4e2d\u5fc5\u987b\u5305\u542b\u56fe\u50cf URL \u548c/\u6216\u6587\u672c\u3002\u5982\u679c\u60a8\u6dfb\u52a0\u56fe\u50cf\uff0c\u8fd8\u5fc5\u987b\u63d0\u4f9b\u63cf\u8ff0\u8be5\u56fe\u50cf\u7684\u66ff\u6362\u6587\u672c\uff0c\u4ee5\u5141\u8bb8\u7528\u6237\u5728\u672a\u52a0\u8f7d\u8be5\u56fe\u50cf\u7684\u60c5\u51b5\u4e0b\u56de\u7b54\u8c03\u67e5\u95ee\u5377\u3002", 
    "You can make limited use of Markdown in answer texts, preferably only bold and italics.": "Markdown \u5728\u7b54\u6848\u6587\u672c\u4e2d\u7684\u5e94\u7528\u53ef\u80fd\u5f88\u6709\u9650\uff0c\u6700\u597d\u4ec5\u9650\u4e8e\u7c97\u4f53\u548c\u659c\u4f53\u3002", 
    "move poll down": "\u4e0b\u79fb\u8c03\u67e5\u95ee\u5377", 
    "move poll up": "\u4e0a\u79fb\u8c03\u67e5\u95ee\u5377"
  };

  django.gettext = function (msgid) {
    var value = django.catalog[msgid];
    if (typeof(value) == 'undefined') {
      return msgid;
    } else {
      return (typeof(value) == 'string') ? value : value[0];
    }
  };

  django.ngettext = function (singular, plural, count) {
    var value = django.catalog[singular];
    if (typeof(value) == 'undefined') {
      return (count == 1) ? singular : plural;
    } else {
      return value[django.pluralidx(count)];
    }
  };

  django.gettext_noop = function (msgid) { return msgid; };

  django.pgettext = function (context, msgid) {
    var value = django.gettext(context + '\x04' + msgid);
    if (value.indexOf('\x04') != -1) {
      value = msgid;
    }
    return value;
  };

  django.npgettext = function (context, singular, plural, count) {
    var value = django.ngettext(context + '\x04' + singular, context + '\x04' + plural, count);
    if (value.indexOf('\x04') != -1) {
      value = django.ngettext(singular, plural, count);
    }
    return value;
  };
  

  django.interpolate = function (fmt, obj, named) {
    if (named) {
      return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
    } else {
      return fmt.replace(/%s/g, function(match){return String(obj.shift())});
    }
  };


  /* formatting library */

  django.formats = {
    "DATETIME_FORMAT": "Y\u5e74n\u6708j\u65e5 H:i", 
    "DATETIME_INPUT_FORMATS": [
      "%Y/%m/%d %H:%M", 
      "%Y-%m-%d %H:%M", 
      "%Y\u5e74%n\u6708%j\u65e5 %H:%M", 
      "%Y/%m/%d %H:%M:%S", 
      "%Y-%m-%d %H:%M:%S", 
      "%Y\u5e74%n\u6708%j\u65e5 %H:%M:%S", 
      "%Y/%m/%d %H:%M:%S.%f", 
      "%Y-%m-%d %H:%M:%S.%f", 
      "%Y\u5e74%n\u6708%j\u65e5 %H:%n:%S.%f", 
      "%Y-%m-%d"
    ], 
    "DATE_FORMAT": "Y\u5e74n\u6708j\u65e5", 
    "DATE_INPUT_FORMATS": [
      "%Y/%m/%d", 
      "%Y-%m-%d", 
      "%Y\u5e74%n\u6708%j\u65e5"
    ], 
    "DECIMAL_SEPARATOR": ".", 
    "FIRST_DAY_OF_WEEK": "1", 
    "MONTH_DAY_FORMAT": "m\u6708j\u65e5", 
    "NUMBER_GROUPING": "4", 
    "SHORT_DATETIME_FORMAT": "Y\u5e74n\u6708j\u65e5 H:i", 
    "SHORT_DATE_FORMAT": "Y\u5e74n\u6708j\u65e5", 
    "THOUSAND_SEPARATOR": "", 
    "TIME_FORMAT": "H:i", 
    "TIME_INPUT_FORMATS": [
      "%H:%M", 
      "%H:%M:%S", 
      "%H:%M:%S.%f"
    ], 
    "YEAR_MONTH_FORMAT": "Y\u5e74n\u6708"
  };

  django.get_format = function (format_type) {
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

}(this));


                  }
                };
                PollXBlockI18N.init();
                global.PollXBlockI18N = PollXBlockI18N;
            }(this));
        