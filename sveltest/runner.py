#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""


                   _  _              _
                  | || |            | |
  ___ __   __ ___ | || |_  ___  ___ | |_
 / __|\ \ / // _ \| || __|/ _ \/ __|| __|
 \__ \ \ V /|  __/| || |_|  __/\__ \| |_
 |___/  \_/  \___||_| \__|\___||___/ \__|



"""

import sys
import time
from concurrent.futures.thread import ThreadPoolExecutor

from typing import Optional, List, Union, Dict, Any, NoReturn, Tuple
from sveltest.bin.conf import settings

import unittest
import warnings
from functools import wraps
from unittest import TestResult

from sveltest.support.logger_v2 import log_v2

from .loader import svelteTestLoader
from rich.console import Console, OverflowMethod

console = Console()

from unittest.signals import registerResult

get_case = getattr(settings, "CASE_SUITE_PATH")


def failfast(method):
    @wraps(method)
    def inner(self, *args, **kw):
        if getattr(self, 'failfast', False):
            self.stop()
        return method(self, *args, **kw)

    return inner


STDOUT_LINE = '\nStdout:\n%s'
STDERR_LINE = '\nStderr:\n%s'


class CommonConfig:
    """"""
    pass


class SvelteResult(TestResult):
    """

    """

    def stopTest(self, test: Optional[object]):
        """

        :param test:
        :return:
        """
        """Called when the given test has been run"""

        setattr(CommonConfig, "run", {
            "count": self.testsRun,
            "errors": len(self.errors),
            "failures": len(self.failures),
            "skipped": len(self.skipped),
        })


class SvelteTestResult(SvelteResult):
    """

    """

    def __init__(self, stream: Optional[Any],
                 descriptions: Optional[str],
                 verbosity: Optional[int],
                 module: Optional[str]):
        """

        :param stream:
        :param descriptions:
        :param verbosity:
        :param module:
        """
        super(SvelteTestResult, self).__init__()
        self.stream = stream
        self.verbosity = verbosity
        self.descriptions = descriptions
        self.module = module

    def addSuccess(self, test:Optional[Any],
                   *args:Optional[Tuple],
                   **kwargs:Optional[Dict]
                   ):
        """

        :param test:
        :param args:
        :param kwargs:
        :return:
        """

        add_success = str(self.module).replace('\\', '/').split('/')[-1].rstrip("'>")

        super(SvelteTestResult, self).addSuccess(test)

        if self.verbosity > 1:
            console.print("%s    %s   PASS" % (add_success, test), style="green")
        elif self.verbosity:
            # ??????
            console.print("%s   OK" % (test), style="green")

    def addError(self, test:Optional[Any], err:Optional[str]):
        """

        :param test:
        :param err:
        :return:
        """

        add_success = str(self.module).replace('\\', '/').split('/')[-1].rstrip("'>")
        super(SvelteTestResult, self).addError(test, err)
        if self.verbosity > 1:
            console.print("%s    %s   ERROR" % (add_success, test), style="green")
        elif self.verbosity:
            # ??????
            console.print("%s   E" % (test), style="green")

    def addFailure(self, test:Optional[Any],err:Optional[str]):
        """

        :param test:
        :param err:
        :return:
        """
        # ???????????????????????????
        add_failure = str(self.module).replace('\\', '/').split('/')[-1].rstrip("'>")
        super(SvelteTestResult, self).addFailure(test, err)
        if self.verbosity > 1:
            console.print("%s    %s   FAIL" % (add_failure, test), style="red")
        elif self.verbosity:
            console.print("%s   F" % (test), style="red")

    def addSkip(self, test: Optional[Any], reason: Optional[str]):
        """

        :param test:
        :param reason:
        :return:
        """
        # overflow_methods: List[OverflowMethod] = ["???????????????"]
        # for overflow in overflow_methods:
        # console.rule(title=overflow_methods[0], characters="-", style='yellow')
        add_skip = str(self.module).replace('\\', '/').split('/')[-1].rstrip("'>")
        super(SvelteTestResult, self).addSkip(test, reason)
        if self.verbosity > 1:
            console.print("%s    %s   SKIP" % (test, reason), style="yellow")

        elif self.verbosity:
            console.print("%s    %s   S" % (test, reason), style="yellow")

    def printErrors(self, e:Optional[int]):
        """

        :param e:
        :return:
        """
        if self.verbosity:
            self.stream.writeln()

        if e != 0:
            overflow_methods: List[OverflowMethod] = ["??????????????????"]
            # for overflow in overflow_methods:
            console.rule(title=overflow_methods[0], characters="-", style='bold blue')
            self.printErrorList('ERROR', self.errors)
            self.printErrorList('FAIL', self.failures)

    def printErrorList(self, flavour:Optional[str], errors:Optional[Any]):
        """

        :param flavour:
        :param errors:
        :return:
        """
        # ????????????????????????

        try:
            for test, err in errors:
                err_f = err
                err_case = err_f.split("\n")[1].split(" ")[3:]
                _path = str(err_case[0].split('"')[1])

                console.print(">>> " + str(test), style="red")
                console.print(err_f, style="red")
        except:

            for test in errors:

                console.print(">>> " + str(test[-1]), style="red")
                for x in str(test[1]).split("\n"):
                    console.print(x, style="red")


class _WritelnDecorator(object):
    """Used to decorate file-like objects with a handy 'writeln' method"""

    def __init__(self, stream):
        self.stream = stream

    def __getattr__(self, attr):
        if attr in ('stream', '__getstate__'):
            raise AttributeError(attr)
        return getattr(self.stream, attr)

    def writeln(self, arg=None):
        if arg:
            self.write(arg)
        self.write('\n')  # text-mode streams translate to \r\n if needed


class SvelteTextTestRunner(object):
    """???????????????????????????????????????????????????
        ???????????????????????????????????????????????????????????????
        ???????????????????????????????????????????????????
    """

    # resultclass =

    def __init__(self, stream: Optional[object] = None,
                 descriptions: Optional[Union[str, bool]] = True,
                 verbosity: Optional[Union[str, int]] = 1,
                 failfast: Optional[bool] = False,
                 buffer: Optional[bool] = False,
                 warnings: Optional[str] = None,
                 *, tb_locals: Optional[bool] = False,
                 module: Optional[Any] = None):
        """
        ????????????TextTestRunner???
        ??????????????????**kwargs??????????????????
        ??????????????????
        :param stream:
        :param descriptions:
        :param verbosity:
        :param failfast:
        :param buffer:
        :param warnings:
        :param tb_locals:
        :param module:
        """

        if stream is None:
            stream = sys.stderr
        self.stream = _WritelnDecorator(stream)
        self.descriptions = descriptions
        self.verbosity = verbosity
        self.failfast = failfast
        self.buffer = buffer
        self.tb_locals = tb_locals
        self.warnings = warnings
        self.module = module

    def run(self, test, max_workers: Optional[int] = 0):
        """

        :param test:
        :return:
        """

        result = SvelteTestResult(stream=self.stream, descriptions=self.descriptions, verbosity=self.verbosity,
                                  module=self.module, )

        if test.countTestCases() > 0:

            overflow_methods: List[OverflowMethod] = ["??????????????????"]
            console.rule(title=overflow_methods[0], characters="=", style='bold blue')

            # "??????????????????????????????????????????."

            registerResult(result)
            result.failfast = self.failfast
            result.buffer = self.buffer
            result.tb_locals = self.tb_locals
            with warnings.catch_warnings():
                if self.warnings:

                    warnings.simplefilter(self.warnings)

                    if self.warnings in ['default', 'always']:
                        warnings.filterwarnings('module',
                                                category=DeprecationWarning,
                                                message=r'Please use assert\w+ instead.')
                startTime = time.perf_counter()
                startTestRun = getattr(result, 'startTestRun', None)

                if startTestRun is not None:
                    startTestRun()
                try:
                    if max_workers != 0:
                        with ThreadPoolExecutor(max_workers=max_workers) as ts:
                            for suite in test:
                                # ???????????????????????????????????????
                                ts.submit(suite.run, result=result)
                    else:
                        test(result)

                finally:
                    stopTestRun = getattr(result, 'stopTestRun', None)
                    if stopTestRun is not None:
                        stopTestRun()
                stopTime = time.perf_counter()

            timeTaken = stopTime - startTime

            get_run_test = getattr(CommonConfig, "run")
            count_test_success = get_run_test["count"] - (
                    get_run_test["errors"] + get_run_test["failures"] + get_run_test["skipped"]
            )

            result.printErrors(get_run_test["errors"] + get_run_test["failures"])

            run = result.testsRun

            overflow_methods: List[OverflowMethod] = ["??????????????????"]
            console.rule(title=overflow_methods[0], characters="*", style='bold blue')

            from rich.table import Table
            table = Table(title="????????????", show_header=True, header_style="bold yellow")
            table.add_column('status', no_wrap=True)
            table.add_column('count', no_wrap=True)

            data = [
                ['PASS', str(count_test_success)],
                ['FAIL', str(get_run_test["failures"])],
                ['SKIP', str(get_run_test["skipped"])],
                ['ERROR', str(get_run_test["errors"])],
                ['COUNT', str(get_run_test["count"])],

            ]

            for case in data:
                table.add_row(case[0], case[1])
            console.print(table)

            case_stop = "??????????????? %d ???????????????  ??????????????? %.3fs" % ((run, timeTaken))
            overflow_methods: List[OverflowMethod] = [case_stop]
            console.rule(title=overflow_methods[0], characters="=", style='bold blue')

            expectedFails = unexpectedSuccesses = skipped = 0
            try:
                results = map(len, (result.expectedFailures,
                                    result.unexpectedSuccesses,
                                    result.skipped))
            except AttributeError:
                pass
            else:
                expectedFails, unexpectedSuccesses, skipped = results

            infos = []
            if not result.wasSuccessful():

                failed, errored = len(result.failures), len(result.errors)
                if failed:
                    infos.append("failed=%d" % failed)
                if errored:
                    infos.append("errored=%d" % errored)

            if skipped:
                infos.append("skipped=%d" % skipped)
            if expectedFails:
                infos.append("expectedFails=%d" % expectedFails)
            if unexpectedSuccesses:
                infos.append("unexpected successes=%d" % unexpectedSuccesses)

            return result

        else:
            log_v2.warning("????????????????????????????????????")


class SvelteMain(object):
    """

    """

    def __init__(self, run_case_path: Optional[Any] = "__main__",
                 debug: Optional[bool] = True,
                 verbosity: Optional[int] = 1, failfast: Optional[Union[str, bool, int]] = None,
                 title: Optional[str] = "sveltest Test Report", tester: Optional[str] = "Anonymous",
                 description: Optional[str] = "Test case execution",
                 save_last_try: Optional[bool] = False,
                 thread_count: int = 0
                 ):
        """"""

        self.path = run_case_path
        self.debug = debug
        self.title = title
        self.tester = tester
        self.description = description
        self.verbosity = verbosity
        self.failfast = failfast
        # ???????????????????????????
        # self.exec_driver = exec_driver
        self.runner = unittest.TextTestRunner
        self.report = None
        self.save_last_try = save_last_try
        # ???????????????
        self.testSuites = []
        self.thread_count = thread_count

        self.module = __import__(self.path)

        if self.path:

            if self.debug is False or getattr(settings, "DEBUG") is False:

                if settings.CASE_SUITE_PATH:
                    case = unittest.defaultTestLoader.discover(start_dir=settings.CASE_SUITE_PATH,
                                                               pattern=settings.TEST_CASE_ENFORCE_RULES)

                else:
                    raise Exception("????????????manage.py???????????????DEBUG??????????????????")


            else:
                case = svelteTestLoader.loadTestsFromModule(self.module)

            self.run(case)

    def run(self, suits: Optional[Any]) -> NoReturn:
        """
        run test case
        """
        if self.debug is True and getattr(settings, "DEBUG") is True:
            # debug ?????????????????????????????????????????????
            testrunner = SvelteTextTestRunner(
                verbosity=self.verbosity,
                failfast=self.failfast,
                module=self.module
                # buffer=self.buffer,
                # warnings=self.warnings,
                # tb_locals=self.tb_locals
            )
            testrunner.run(
                test=suits, max_workers=self.thread_count
            )

        if self.debug is False or getattr(settings, "DEBUG") is False:
            #
            from sveltest.bin.conf.commandline import MainTestSuite
            MainTestSuite().test_suite_base(
                suites=suits,
                test_title_name=self.title, description=self.description, thread_count=self.thread_count,
                save_last_try=True
            )


main = SvelteMain


