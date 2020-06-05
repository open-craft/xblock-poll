
            (function(global){
                var PollXBlockI18N = {
                  init: function() {
                    

(function (globals) {

  var django = globals.django || (globals.django = {});

  
  django.pluralidx = function (count) { return (count == 1) ? 0 : 1; };
  

  
  /* gettext library */

  django.catalog = {
    "Answer": "\u56de\u7b54", 
    "Delete": "\u524a\u9664", 
    "Feedback": "\u30d5\u30a3\u30fc\u30c9\u30d0\u30c3\u30af", 
    "Image URL": "\u753b\u50cfURL", 
    "Image alternative text": "\u753b\u50cf\u4ee3\u66ff\u30c6\u30ad\u30b9\u30c8", 
    "Question": "\u8cea\u554f", 
    "Results": "\u7d50\u679c", 
    "Results gathered from {total} respondent.": [
      "\u56de\u7b54\u8005{total}\u4eba\u304b\u3089\u53ce\u96c6\u3057\u305f\u7d50\u679c\u3002", 
      "\u56de\u7b54\u8005{total}\u4eba\u304b\u3089\u53ce\u96c6\u3057\u305f\u7d50\u679c\u3002"
    ], 
    "Submit": "\u9001\u4fe1",
    "This must have an image URL or text, and can have both.  If you add an image, you must also provide an alternative text that describes the image in a way that would allow someone to answer the poll if the image did not load.": "\u3053\u3053\u306b\u306f\u3001\u753b\u50cfURL\u307e\u305f\u306f\u30c6\u30ad\u30b9\u30c8\u3001\u3042\u308b\u3044\u306f\u305d\u306e\u4e21\u65b9\u3092\u5165\u529b\u3057\u307e\u3059\u3002\u753b\u50cf\u3092\u8ffd\u52a0\u3057\u305f\u5834\u5408\u306f\u3001\u753b\u50cf\u304c\u8aad\u307f\u8fbc\u3081\u306a\u304b\u3063\u305f\u5834\u5408\u3067\u3082\u56de\u7b54\u8005\u304c\u6295\u7968\u8abf\u67fb\u3067\u56de\u7b54\u3067\u304d\u308b\u3088\u3046\u306b\u3001\u753b\u50cf\u3092\u8aac\u660e\u3059\u308b\u4ee3\u66ff\u30c6\u30ad\u30b9\u30c8\u3082\u5165\u529b\u3057\u306a\u3051\u308c\u3070\u306a\u308a\u307e\u305b\u3093\u3002", 
    "You can make limited use of Markdown in answer texts, preferably only bold and italics.": "\u56de\u7b54\u30c6\u30ad\u30b9\u30c8\u3067\u30de\u30fc\u30af\u30c0\u30a6\u30f3\u3092\u9650\u5b9a\u7684\u306b\u4f7f\u7528\u3067\u304d\u307e\u3059\u3002\u305f\u3060\u3057\u3001\u3067\u304d\u308c\u3070\u592a\u5b57\u3068\u30a4\u30bf\u30ea\u30c3\u30af\u4f53\u306e\u307f\u306e\u4f7f\u7528\u3068\u3057\u307e\u3059\u3002", 
    "move poll down": "\u6295\u7968\u7dcf\u6570\u3092\u4e0b\u3052\u308b", 
    "move poll up": "\u6295\u7968\u7dcf\u6570\u3092\u4e0a\u3052\u308b"
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
    "DATETIME_FORMAT": "Y\u5e74n\u6708j\u65e5G:i", 
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
    "DATE_FORMAT": "Y\u5e74n\u6708j\u65e5", 
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
    "DECIMAL_SEPARATOR": ".", 
    "FIRST_DAY_OF_WEEK": "0", 
    "MONTH_DAY_FORMAT": "n\u6708j\u65e5", 
    "NUMBER_GROUPING": "0", 
    "SHORT_DATETIME_FORMAT": "Y/m/d G:i", 
    "SHORT_DATE_FORMAT": "Y/m/d", 
    "THOUSAND_SEPARATOR": ",", 
    "TIME_FORMAT": "G:i", 
    "TIME_INPUT_FORMATS": [
      "%H:%M:%S", 
      "%H:%M:%S.%f", 
      "%H:%M"
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
        