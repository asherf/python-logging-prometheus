import unittest
import logging
from prometheus_client import REGISTRY
import logging_prometheus


class TestLoggingPrometheus(unittest.TestCase):
    def test_rootLoggerExports(self):
        logging.error('There was an error.')
        assert REGISTRY.get_sample_value('python_logging_messages_total',
                                         labels={'logger': 'test_levels',
                                                 'level': 'ERROR'}) == 1

    def test_all_levels(self):
        logger = logging.getLogger('test_levels')
        logger.setLevel(logging.DEBUG)
        logger.debug('debug message')
        logger.info('info message')
        logger.warning('warn message')
        logger.error('error message')
        logger.critical('critical message')
        for level in ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'):
            lables = {'logger': 'test_levels', 'level': level}
            assert REGISTRY.get_sample_value('python_logging_messages_total', labels=lables) == 1

    def test_setLevel(self):
        logger = logging.getLogger('test_setLevel')
        logger.setLevel(logging.CRITICAL)
        logger.debug('debug message')
        logger.info('info message')
        logger.warning('warn message')
        logger.error('error message')
        logger.critical('critical message')
        for level in ('DEBUG', 'INFO', 'WARNING', 'ERROR'):
            lables = {'logger': 'test_setLevel', 'level': level}
            assert REGISTRY.get_sample_value('python_logging_messages_total', labels=lables) is None
            lables = {'logger': 'test_levels', 'level': 'CRITICAL'}
            assert REGISTRY.get_sample_value('python_logging_messages_total', labels=lables) == 1
