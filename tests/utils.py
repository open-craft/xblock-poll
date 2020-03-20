# Test mocks and helpers
from __future__ import absolute_import
from webob import Request
from xblock.runtime import DictKeyValueStore, KvsFieldData
from xblock.test.tools import TestRuntime


def make_request(body, method='POST'):
    """
    Helper method to make request
    """
    request = Request.blank('/')
    request.body = body.encode('utf-8')
    request.method = method
    return request

# pylint: disable=abstract-method
class MockRuntime(TestRuntime):
    """
    Provides a mock XBlock runtime object.
    """
    def __init__(self, **kwargs):
        field_data = kwargs.get('field_data', KvsFieldData(DictKeyValueStore()))
        super(MockRuntime, self).__init__(field_data=field_data)
