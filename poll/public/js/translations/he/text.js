
            (function(global){
                var PollXBlockI18N = {
                  init: function() {
                    

(function (globals) {

  var django = globals.django || (globals.django = {});

  
  django.pluralidx = function (n) {
    var v=(n != 1);
    if (typeof(v) == 'boolean') {
      return v ? 1 : 0;
    } else {
      return v;
    }
  };
  

  
  /* gettext library */

  django.catalog = {
    "'{field}' is not present, or not a JSON array.": "'{field}' \u05d0\u05d9\u05e0\u05d5 \u05e0\u05de\u05e6\u05d0, \u05d0\u05d5 \u05d0\u05d9\u05e0\u05d5 \u05d1\u05de\u05e2\u05e8\u05da JSON.", 
    "All images must have an alternative text describing the image in a way that would allow someone to answer the poll if the image did not load.": "\u05dc\u05db\u05dc \u05d4\u05ea\u05de\u05d5\u05e0\u05d5\u05ea \u05d7\u05d9\u05d9\u05d1 \u05dc\u05d4\u05d9\u05d5\u05ea \u05d8\u05e7\u05e1\u05d8 \u05d7\u05dc\u05d5\u05e4\u05d9 \u05d4\u05de\u05ea\u05d0\u05e8 \u05d0\u05ea \u05d4\u05ea\u05de\u05d5\u05e0\u05d4 \u05db\u05da \u05e9\u05d9\u05ea\u05d0\u05e4\u05e9\u05e8 \u05dc\u05de\u05d9\u05e9\u05d4\u05d5 \u05dc\u05e2\u05e0\u05d5\u05ea \u05e2\u05dc \u05d4\u05e1\u05e7\u05e8 \u05d1\u05de\u05d9\u05d3\u05d4 \u05d5\u05d4\u05ea\u05de\u05d5\u05e0\u05d4 \u05d0\u05d9\u05e0\u05d4 \u05e2\u05d5\u05dc\u05d4.", 
    "Answer": "\u05ea\u05e9\u05d5\u05d1\u05d4", 
    "Answer choices for this Survey": "\u05d0\u05e4\u05e9\u05e8\u05d5\u05d9\u05d5\u05ea \u05d4\u05ea\u05e9\u05d5\u05d1\u05d4 \u05dc\u05e1\u05e7\u05e8 \u05d6\u05d4", 
    "Answer not included with request.": "\u05d4\u05ea\u05e9\u05d5\u05d1\u05d4 \u05d0\u05d9\u05e0\u05e0\u05d4 \u05db\u05dc\u05d5\u05dc\u05d4 \u05d1\u05d1\u05e7\u05e9\u05d4.", 
    "Are you enjoying the course?": "\u05d4\u05d0\u05dd \u05d0\u05ea\u05d4 \u05e0\u05d4\u05e0\u05d4 \u05de\u05d4\u05e7\u05d5\u05e8\u05e1?", 
    "Blue": "\u05db\u05d7\u05d5\u05dc", 
    "Delete": "\u05de\u05d7\u05e7", 
    "Do you think you will learn a lot?": "\u05d4\u05d0\u05dd \u05dc\u05d3\u05e2\u05ea\u05da \u05ea\u05dc\u05de\u05d3 \u05d4\u05e8\u05d1\u05d4?", 
    "Found unknown answer '{answer_key}' for question key '{question_key}'": "\u05e0\u05de\u05e6\u05d0\u05d4 \u05ea\u05e9\u05d5\u05d1\u05d4 \u05dc\u05d0 \u05de\u05d5\u05db\u05e8\u05ea '{answer_key}' \u05e2\u05d1\u05d5\u05e8 \u05de\u05e4\u05ea\u05d7 \u05d4\u05e9\u05d0\u05dc\u05d4 '{question_key}'", 
    "Image URL": "\u05db\u05ea\u05d5\u05d1\u05ea URL \u05e9\u05dc \u05ea\u05de\u05d5\u05e0\u05d4", 
    "Image alternative text": "\u05d8\u05e7\u05e1\u05d8 \u05d7\u05dc\u05d5\u05e4\u05d9 \u05dc\u05ea\u05de\u05d5\u05e0\u05d4", 
    "Maximum Submissions missing or not an integer.": "\u05d7\u05e1\u05e8 \u05de\u05e1\u05e4\u05e8 \u05e9\u05dc\u05d9\u05d7\u05d5\u05ea \u05de\u05e8\u05d1\u05d9 \u05d0\u05d5 \u05e9\u05d0\u05d9\u05e0\u05d5 \u05de\u05e1\u05e4\u05e8 \u05e9\u05dc\u05dd.", 
    "Maybe": "\u05d0\u05d5\u05dc\u05d9", 
    "No": "\u05dc\u05d0", 
    "No key \"{choice}\" in answers table.": "\u05d0\u05d9\u05df \u05de\u05e4\u05ea\u05d7 \"{choice}\" \u05d1\u05d8\u05d1\u05dc\u05ea \u05d4\u05ea\u05e9\u05d5\u05d1\u05d5\u05ea.", 
    "Not all questions were included, or unknown questions were included. Try refreshing and trying again.": "\u05dc\u05d0 \u05e0\u05db\u05dc\u05dc\u05d5 \u05db\u05dc \u05d4\u05e9\u05d0\u05dc\u05d5\u05ea \u05d0\u05d5 \u05e9\u05d4\u05d5\u05e6\u05d2\u05d5 \u05e9\u05d0\u05dc\u05d5\u05ea \u05dc\u05d0 \u05de\u05d5\u05db\u05e8\u05d5\u05ea. \u05e8\u05e2\u05e0\u05df \u05d5\u05e0\u05e1\u05d4 \u05e9\u05e0\u05d9\u05ea.", 
    "Number of times the user has sent a submission.": "\u05de\u05e1\u05e4\u05e8 \u05d4\u05e4\u05e2\u05de\u05d9\u05dd \u05e9\u05e9\u05dc\u05d7 \u05d4\u05de\u05e9\u05ea\u05de\u05e9 \u05d4\u05d2\u05e9\u05d4.", 
    "Other": "\u05d0\u05d7\u05e8", 
    "Poll": "\u05de\u05b4\u05e9\u05d0\u05dc", 
    "Private results may not be False when Maximum Submissions is not 1.": "\u05ea\u05e9\u05d5\u05d1\u05d5\u05ea \u05d0\u05d9\u05e9\u05d9\u05d5\u05ea \u05d0\u05d9\u05e0\u05df \u05d9\u05db\u05d5\u05dc\u05d5\u05ea \u05dc\u05d4\u05d9\u05d5\u05ea '\u05dc\u05d0 \u05e0\u05db\u05d5\u05df' \u05db\u05d0\u05e9\u05e8 \u05de\u05e1\u05e4\u05e8 \u05d4\u05e9\u05dc\u05d9\u05d7\u05d5\u05ea \u05d4\u05de\u05e8\u05d1\u05d9 \u05d0\u05d9\u05e0\u05d5 1.", 
    "Question": "\u05e9\u05d0\u05dc\u05d4", 
    "Questions for this Survey": "\u05e9\u05d0\u05dc\u05d5\u05ea \u05dc\u05e1\u05e7\u05e8 \u05d6\u05d4", 
    "Red": "\u05d0\u05d3\u05d5\u05dd", 
    "Results gathered from {total} respondent.": "\u05ea\u05e9\u05d5\u05d1\u05d5\u05ea \u05e9\u05e0\u05d0\u05e1\u05e4\u05d5 \u05de{total} \u05e2\u05d5\u05e0\u05d4.", 
    "Results gathered from {total} respondents.": "\u05ea\u05e9\u05d5\u05d1\u05d5\u05ea \u05e9\u05e0\u05d0\u05e1\u05e4\u05d5 \u05de{total} \u05e2\u05d5\u05e0\u05d9\u05dd.", 
    "Survey": "\u05e1\u05e7\u05e8", 
    "Text to display after the user votes.": "\u05d4\u05d8\u05e7\u05e1\u05d8 \u05e9\u05d9\u05d5\u05e6\u05d2 \u05dc\u05d0\u05d7\u05e8 \u05d4\u05e6\u05d1\u05e2\u05ea \u05d4\u05de\u05e9\u05ea\u05de\u05e9.", 
    "The answer options on this poll.": "\u05d0\u05e4\u05e9\u05e8\u05d5\u05d9\u05d5\u05ea \u05d4\u05ea\u05e9\u05d5\u05d1\u05d4 \u05dc\u05de\u05e9\u05d0\u05dc \u05d6\u05d4.", 
    "The maximum number of times a user may send a submission.": "\u05de\u05e1\u05e4\u05e8 \u05d4\u05e4\u05e2\u05de\u05d9\u05dd \u05d4\u05de\u05e8\u05d1\u05d9 \u05e9\u05d9\u05db\u05d5\u05dc \u05de\u05e9\u05ea\u05de\u05e9 \u05dc\u05e9\u05dc\u05d5\u05d7 \u05d4\u05d2\u05e9\u05d4.", 
    "The student's answer": "\u05ea\u05e9\u05d5\u05d1\u05ea \u05d4\u05e1\u05d8\u05d5\u05d3\u05e0\u05d8", 
    "The user's answers": "\u05ea\u05e9\u05d5\u05d1\u05d5\u05ea \u05d4\u05de\u05e9\u05ea\u05de\u05e9", 
    "This must have an image URL or text, and can have both.  If you add an image, you must also provide an alternative text that describes the image in a way that would allow someone to answer the poll if the image did not load.": "\u05d7\u05d9\u05d9\u05d1\u05ea \u05dc\u05d4\u05d9\u05d5\u05ea \u05db\u05ea\u05d5\u05d1\u05ea URL \u05e9\u05dc \u05ea\u05de\u05d5\u05e0\u05d4 \u05d0\u05d5 \u05d8\u05e7\u05e1\u05d8, \u05d5\u05d9\u05db\u05d5\u05dc\u05d9\u05dd \u05dc\u05d4\u05d9\u05d5\u05ea \u05e9\u05e0\u05d9\u05d4\u05dd.  \u05d1\u05d4\u05d5\u05e1\u05e4\u05ea \u05ea\u05de\u05d5\u05e0\u05d4, \u05e2\u05dc\u05d9\u05da \u05dc\u05e1\u05e4\u05e7 \u05d8\u05e7\u05e1\u05d8 \u05d7\u05dc\u05d5\u05e4\u05d9 \u05d4\u05de\u05ea\u05d0\u05e8 \u05d0\u05ea \u05d4\u05ea\u05de\u05d5\u05e0\u05d4 \u05db\u05da \u05e9\u05ea\u05d0\u05e4\u05e9\u05e8 \u05dc\u05de\u05d9\u05e9\u05d4\u05d5 \u05dc\u05e2\u05e0\u05d5\u05ea \u05e2\u05dc \u05d4\u05e1\u05e7\u05e8 \u05d0\u05dd \u05d4\u05ea\u05de\u05d5\u05e0\u05d4 \u05d0\u05d9\u05e0\u05d4 \u05e2\u05d5\u05dc\u05d4.", 
    "Total tally of answers from students.": "\u05de\u05e1\u05e4\u05e8 \u05db\u05d5\u05dc\u05dc \u05e9\u05dc \u05ea\u05e9\u05d5\u05d1\u05d5\u05ea \u05d4\u05e1\u05d8\u05d5\u05d3\u05e0\u05d8\u05d9\u05dd.", 
    "What is your favorite color?": "\u05de\u05d4\u05d5 \u05d4\u05e6\u05d1\u05e2 \u05d4\u05d0\u05d4\u05d5\u05d1 \u05e2\u05dc\u05d9\u05da?", 
    "Whether or not to display results to the user.": "\u05d4\u05d0\u05dd \u05dc\u05d4\u05e6\u05d9\u05d2 \u05ea\u05d5\u05e6\u05d0\u05d5\u05ea \u05dc\u05de\u05e9\u05ea\u05de\u05e9.", 
    "Would you recommend this course to your friends?": "\u05d4\u05d0\u05dd \u05d4\u05d9\u05d9\u05ea \u05de\u05de\u05dc\u05d9\u05e5 \u05e2\u05dc \u05e7\u05d5\u05e8\u05e1 \u05d6\u05d4 \u05dc\u05d7\u05d1\u05e8\u05d9\u05da?", 
    "Yes": "\u05db\u05df", 
    "You can make limited use of Markdown in answer texts, preferably only bold and italics.": "\u05ea\u05d5\u05db\u05dc \u05dc\u05d4\u05e9\u05ea\u05de\u05e9 \u05d1\u05d0\u05d5\u05e4\u05df \u05de\u05d5\u05d2\u05d1\u05dc \u05d1-Markdown \u05d1\u05ea\u05e9\u05d5\u05d1\u05ea \u05d8\u05e7\u05e1\u05d8, \u05e2\u05d3\u05d9\u05e3 \u05d1\u05d0\u05d5\u05ea\u05d9\u05d5\u05ea \u05d1\u05d5\u05dc\u05d8\u05d5\u05ea \u05d5\u05e0\u05d8\u05d5\u05d9\u05d5\u05ea.", 
    "You have already voted as many times as you are allowed.": "\u05db\u05d1\u05e8 \u05d4\u05e6\u05d1\u05e2\u05ea \u05d0\u05ea \u05de\u05e1\u05e4\u05e8 \u05d4\u05e4\u05e2\u05de\u05d9\u05dd \u05d4\u05de\u05d5\u05ea\u05e8 \u05dc\u05da.", 
    "You have already voted in this poll.": "\u05db\u05d1\u05e8 \u05d4\u05e6\u05d1\u05e2\u05ea \u05d1\u05e1\u05e7\u05e8 \u05d6\u05d4.", 
    "You must include at least one {noun_lower}.": "\u05d7\u05d5\u05d1\u05d4 \u05dc\u05db\u05dc\u05d5\u05dc \u05dc\u05e4\u05d7\u05d5\u05ea \u05d0\u05d7\u05ea {noun_lower}.", 
    "You must specify a question.": "\u05e2\u05dc\u05d9\u05da \u05dc\u05e6\u05d9\u05d9\u05df \u05e9\u05d0\u05dc\u05d4.", 
    "move poll down": "\u05d4\u05e2\u05d1\u05e8 \u05d0\u05ea \u05d4\u05de\u05e9\u05d0\u05dc \u05dc\u05de\u05d8\u05d4", 
    "move poll up": "\u05d4\u05e2\u05d1\u05e8 \u05d0\u05ea \u05d4\u05de\u05e9\u05d0\u05dc \u05dc\u05de\u05e2\u05dc\u05d4", 
    "{noun} has no text or img. Please make sure all {noun_lower}s have one or the other, or both.": "\u05dc{noun} \u05d0\u05d9\u05df \u05d8\u05e7\u05e1\u05d8 \u05d0\u05d5 \u05ea\u05de\u05d5\u05e0\u05d4. \u05d5\u05d3\u05d0 \u05db\u05d9 \u05dc\u05db\u05dc {noun_lower} \u05d9\u05e9 \u05d0\u05d7\u05d3 \u05de\u05d4\u05dd \u05d0\u05d5 \u05d0\u05ea \u05e9\u05e0\u05d9\u05d4\u05dd.", 
    "{noun} was added with no label. All {noun_lower}s must have labels. Please check the form. Check the form and explicitly delete {noun_lower}s if not needed.": "{noun} \u05d4\u05d5\u05e1\u05b7\u05e3 \u05dc\u05dc\u05d0 \u05ea\u05d5\u05d5\u05d9\u05ea. \u05d7\u05d9\u05d9\u05d1\u05d5\u05ea \u05dc\u05d4\u05d9\u05d5\u05ea \u05ea\u05d5\u05d5\u05d9\u05d5\u05ea \u05dc\u05db\u05dc {noun_lower} . \u05e0\u05d0 \u05d1\u05d3\u05d5\u05e7 \u05d0\u05ea \u05d4\u05d8\u05d5\u05e4\u05e1. \u05d1\u05d3\u05d5\u05e7 \u05d0\u05ea \u05d4\u05d8\u05d5\u05e4\u05e1 \u05d5\u05de\u05d7\u05e7 \u05d0\u05ea {noun_lower} \u05e9\u05d0\u05d9\u05e0\u05dd \u05e0\u05d3\u05e8\u05e9\u05d9\u05dd.", 
    "{noun} {item} contains no key.": "{noun} {item} \u05d0\u05d9\u05e0\u05d5 \u05de\u05db\u05d9\u05dc \u05de\u05e4\u05ea\u05d7.", 
    "{noun} {item} not a javascript object!": "{noun} {item} \u05d0\u05d9\u05e0\u05d5 \u05d0\u05d5\u05d1\u05d9\u05d9\u05e7\u05d8 javascript!"
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
    "DATETIME_FORMAT": "j \u05d1F Y H:i", 
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
    "DATE_FORMAT": "j \u05d1F Y", 
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
    "MONTH_DAY_FORMAT": "j \u05d1F", 
    "NUMBER_GROUPING": "0", 
    "SHORT_DATETIME_FORMAT": "d/m/Y H:i", 
    "SHORT_DATE_FORMAT": "d/m/Y", 
    "THOUSAND_SEPARATOR": ",", 
    "TIME_FORMAT": "H:i", 
    "TIME_INPUT_FORMATS": [
      "%H:%M:%S", 
      "%H:%M:%S.%f", 
      "%H:%M"
    ], 
    "YEAR_MONTH_FORMAT": "F Y"
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
        