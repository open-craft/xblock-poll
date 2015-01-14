# XBlock-Poll

> A user-friendly way to query students.

## Introduction

This XBlock enables a course author to create survey/poll elements to get
feedback from students. The XBlocks can either be *poll* or *survey* XBlocks. *Poll* XBlocks have one
question, and a series of answers. *Survey* XBlocks have several questions and a handful of (terse) answers that
a student is expect to answer each one from (Such as 'True', and 'False', or 'Agree' or 'Disagree')

## Features

Survey and Poll are both designed to minimize the amount of fiddling a course author will have to
do in order to create the user experience they desire. By default, answers in polls and questions in surveys
are able to be enhanced with markdown (though it is not recommended to do more than line formatting with it)
and images. Formatting for images is handled by the XBlock's formatters to keep a consistent and sane user experience.

The feedback section of a poll or survey is shown after a user has completed the block. It, along with a poll block's
question field, are intended to make full use of markdown.

## Notes

A poll or survey should not be deployed until its construction is finalized. Changing an answer or question can
cause previous respondent's answers to remap and give an inaccurate picture of the responses.

If a poll has changed enough that it leaves a previous voter's choice ambiguous, their response will be eliminated
from the tally upon their next visit, and they will be permitted to vote again. However, they will not lose progress
or their score.

Things that could make a poll's previous answers ambiguous include adding or removing a question, or adding or
removing an answer.

## Grading

Each block has a score value of 1, credited to the student upon completion of the block.

## Analytics

Two events are fired by the XBlocks-- one for viewing the results of a poll, and one for submitting the user's choice.

The resulting events look like this for polls:

    {"username": "staff", "host": "precise64", "event_source": "server", "event_type": "xblock.poll.submitted", "context": {"course_user_tags": {}, "user_id": 1, "org_id": "JediAcademy", "module": {"display_name": "Poll"}, "course_id": "JediAcademy/FW301/2015", "path": "/courses/JediAcademy/FW301/2015/xblock/i4x:;_;_JediAcademy;_FW301;_poll;_2d25e451be884aa7a15b33860d7c9647/handler/vote"}, "time": "2015-01-12T19:13:39.199098+00:00", "ip": "10.0.2.2", "event": {"url_name": "2d25e451be884aa7a15b33860d7c9647", "choice": "B"}, "agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:34.0) Gecko/20100101 Firefox/34.0", "page": "x_module"}
    {"username": "staff", "host": "precise64", "event_source": "server", "event_type": "xblock.poll.view_results", "context": {"course_user_tags": {}, "user_id": 1, "org_id": "JediAcademy", "module": {"display_name": "Poll"}, "course_id": "JediAcademy/FW301/2015", "path": "/courses/JediAcademy/FW301/2015/xblock/i4x:;_;_JediAcademy;_FW301;_poll;_2d25e451be884aa7a15b33860d7c9647/handler/get_results"}, "time": "2015-01-12T19:13:39.474514+00:00", "ip": "10.0.2.2", "event": {}, "agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:34.0) Gecko/20100101 Firefox/34.0", "page": "x_module"}

...And like this for surveys:

    {"username": "staff", "host": "precise64", "event_source": "server", "event_type": "xblock.survey.submitted", "context": {"course_user_tags": {}, "user_id": 1, "org_id": "JediAcademy", "module": {"display_name": "Survey"}, "course_id": "JediAcademy/FW301/2015", "path": "/courses/JediAcademy/FW301/2015/xblock/i4x:;_;_JediAcademy;_FW301;_survey;_e4975240b6c64a1e988bad86ea917070/handler/vote"}, "time": "2015-01-12T19:13:13.115038+00:00", "ip": "10.0.2.2", "event": {"url_name": "e4975240b6c64a1e988bad86ea917070", "choices": {"enjoy": "Y", "learn": "M", "recommend": "N"}}, "agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:34.0) Gecko/20100101 Firefox/34.0", "page": "x_module"}
    {"username": "staff", "host": "precise64", "event_source": "server", "event_type": "xblock.survey.view_results", "context": {"course_user_tags": {}, "user_id": 1, "org_id": "JediAcademy", "module": {"display_name": "Survey"}, "course_id": "JediAcademy/FW301/2015", "path": "/courses/JediAcademy/FW301/2015/xblock/i4x:;_;_JediAcademy;_FW301;_survey;_e4975240b6c64a1e988bad86ea917070/handler/get_results"}, "time": "2015-01-12T19:13:13.513909+00:00", "ip": "10.0.2.2", "event": {}, "agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:34.0) Gecko/20100101 Firefox/34.0", "page": "x_module"}

