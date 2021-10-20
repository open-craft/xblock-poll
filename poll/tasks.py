from __future__ import absolute_import
import time

from celery import current_app  # pylint: disable=import-error

from lms.djangoapps.instructor_task.models import ReportStore  # pylint: disable=import-error
from opaque_keys.edx.keys import CourseKey, UsageKey  # pylint: disable=import-error
from xmodule.modulestore.django import modulestore  # pylint: disable=import-error


@current_app.task(name='poll.tasks.export_csv_data')
def export_csv_data(block_id, course_id):
    """
    Exports student answers to all supported questions to a CSV file.
    """

    src_block = modulestore().get_item(UsageKey.from_string(block_id))

    start_timestamp = time.time()
    course_key = CourseKey.from_string(course_id)

    filename = src_block.get_filename()

    report_store = ReportStore.from_config(config_name='GRADES_DOWNLOAD')
    report_store.store_rows(course_key, filename, src_block.prepare_data())

    generation_time_s = time.time() - start_timestamp

    return {
        "error": None,
        "report_filename": filename,
        "start_timestamp": start_timestamp,
        "generation_time_s": generation_time_s,
    }
