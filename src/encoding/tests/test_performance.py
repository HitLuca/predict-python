import time
import unittest

from django.test import TestCase

from src.core.constants import REGRESSION
from src.encoding.common import encode_label_log
from src.encoding.encoding_container import SIMPLE_INDEX, BOOLEAN, FREQUENCY, COMPLEX, LAST_PAYLOAD, EncodingContainer, \
    ZERO_PADDING, ALL_IN_ONE
from src.labelling.label_container import *
from src.utils.event_attributes import unique_events, get_additional_columns
from src.utils.file_service import get_log


class TestEncoding(TestCase):
    def setUp(self):
        self.log = get_log("log_cache/repairExample.xes")
        # self.log = get_logs("log_cache/BPI Challenge 2017.xes.gz")[0]
        self.label = LabelContainer(NO_LABEL)
        self.add_col = get_additional_columns(self.log)

    def method_self(self, encoding):
        start_time = time.time()
        # log = get_logs("log_cache/repairExample.xes")[0]
        event_names = unique_events(self.log)
        encode_label_log(self.log, encoding, REGRESSION, self.label, event_names=event_names,
                         additional_columns=self.add_col)
        print("Total for %s %s seconds" % (encoding, time.time() - start_time))

    # This is test
    def performance(self):
        encodings = [SIMPLE_INDEX, BOOLEAN, FREQUENCY, COMPLEX, LAST_PAYLOAD]

        # self.method_self(COMPLEX)
        for encoding in encodings:
            self.method_self(encoding)


@unittest.skip("performance test not needed normally")
class TestAgainstNirdizatiTraining(TestCase):
    @staticmethod
    def do_test(encoding):
        start_time = time.time()
        # log = get_logs("log_cache/general_example.xes")[0]
        log = get_log("log_cache/Sepsis Cases - Event Log.xes")
        label = LabelContainer(REMAINING_TIME, add_elapsed_time=True)
        encoding = EncodingContainer(encoding, prefix_length=185, generation_type=ALL_IN_ONE,
                                     padding=ZERO_PADDING)
        event_names = unique_events(log)
        log = encode_label_log(log, encoding, REGRESSION, label, event_names=event_names)
        print(log.shape)
        print("Total for %s %s seconds" % (encoding, time.time() - start_time))

    def test_performance(self):
        encodings = [SIMPLE_INDEX, BOOLEAN, FREQUENCY]

        # self.method_self(COMPLEX)
        for e in encodings:
            self.do_test(e)


@unittest.skip("performance test not needed normally")
class TestTraceLengthTime(TestCase):
    def setUp(self):
        self.label = LabelContainer(NO_LABEL)
        start_time = time.time()
        self.log1 = get_log("log_cache/Sepsis Cases - Event Log.xes.gz")
        print("Total for %s %s seconds" % ("sepsis", time.time() - start_time))
        start_time = time.time()
        self.log2 = get_log("log_cache/financial_log.xes.gz")
        print("Total for %s %s seconds" % ("financial", time.time() - start_time))
        start_time = time.time()
        self.log3 = get_log("log_cache/BPI Challenge 2017.xes.gz")
        print("Total for %s %s seconds" % ("2017", time.time() - start_time))

    def do_test(self, encoding, log):
        start_time = time.time()
        # log = get_logs(log_path)[0]
        add_col = get_additional_columns(log)
        event_names = unique_events(log)
        encoding = EncodingContainer(encoding, prefix_length=20, padding=ZERO_PADDING)
        log = encode_label_log(log, encoding, REGRESSION, self.label, event_names=event_names,
                               additional_columns=add_col)
        print(log.shape)
        print("Total for %s %s seconds" % (encoding.method, time.time() - start_time))

    def test_performance(self):
        encodings = [SIMPLE_INDEX, BOOLEAN, FREQUENCY, COMPLEX, LAST_PAYLOAD]
        logs = [self.log3]
        for l in logs:
            for encoding in encodings:
                self.do_test(encoding, l)
