
            (function(global){
                var PollXBlockI18N = {
                  init: function() {
                    

(function(globals) {

  var django = globals.django || (globals.django = {});

  
  django.pluralidx = function(count) { return (count == 1) ? 0 : 1; };
  

  /* gettext library */

  django.catalog = django.catalog || {};
  
  var newcatalog = {
    "Answer": "Odpowied\u017a", 
    "Delete": "Usu\u0144", 
    "Feedback": "Informacja zwrotna", 
    "Image URL": "URL obrazu", 
    "Image alternative text": "Tekst alternatywny obrazu", 
    "Question": "Pytanie", 
    "Results": "Wyniki", 
    "Results gathered from {total} respondent.": [
      "Wyniki zebrane od {total} respondenta.", 
      "Wyniki zebrane od {total} respondent\u00f3w."
    ], 
    "Submit": "Prze\u015blij", 
    "This must have an image URL or text, and can have both.  If you add an image, you must also provide an alternative text that describes the image in a way that would allow someone to answer the poll if the image did not load.": "Wymagany jest URL obrazu, tekst lub oba parametry. Je\u015bli dodajesz obraz, musisz te\u017c okre\u015bli\u0107 tekst alternatywny, kt\u00f3re opisuje obraz w taki spos\u00f3b, \u017ceby respondent m\u00f3g\u0142 odpowiedzie\u0107 na pytanie, nawet je\u015bli obraz si\u0119 nie wczyta.", 
    "You can make limited use of Markdown in answer texts, preferably only bold and italics.": "Nie mo\u017cesz w pe\u0142ni u\u017cywasz znacznik\u00f3w Markdown w tek\u015bcie odpowiedzi, u\u017cywaj g\u0142\u00f3wnie znacznik\u00f3w pogrubienia i kursywy.", 
    "move poll down": "przesu\u0144 sonda\u017c w d\u00f3\u0142", 
    "move poll up": "przesu\u0144 sonda\u017c do g\u00f3ry"
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
    "DATETIME_FORMAT": "j E Y H:i", 
    "DATETIME_INPUT_FORMATS": [
      "%d.%m.%Y %H:%M:%S", 
      "%d.%m.%Y %H:%M:%S.%f", 
      "%d.%m.%Y %H:%M", 
      "%d.%m.%Y", 
      "%Y-%m-%d %H:%M:%S", 
      "%Y-%m-%d %H:%M:%S.%f", 
      "%Y-%m-%d %H:%M", 
      "%Y-%m-%d"
    ], 
    "DATE_FORMAT": "j E Y", 
    "DATE_INPUT_FORMATS": [
      "%d.%m.%Y", 
      "%d.%m.%y", 
      "%y-%m-%d", 
      "%Y-%m-%d"
    ], 
    "DECIMAL_SEPARATOR": ",", 
    "FIRST_DAY_OF_WEEK": "1", 
    "MONTH_DAY_FORMAT": "j F", 
    "NUMBER_GROUPING": "3", 
    "SHORT_DATETIME_FORMAT": "d-m-Y  H:i", 
    "SHORT_DATE_FORMAT": "d-m-Y", 
    "THOUSAND_SEPARATOR": "\u00a0", 
    "TIME_FORMAT": "H:i", 
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
        