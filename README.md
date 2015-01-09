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

Each block has a score value of 1, credited to the student upon creation of the block.

