import sys
from datetime import datetime, timezone
import logging
# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
# logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
# logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

class Checker:
    def __init__(self):
        self.checks_passed = 0
        self.checks_failed = 0

    def check(self, cond, message="", raise_exception=False):
        if cond:
            logging.info(f"PASSED check. {message}")
            self.checks_passed += 1
        else:
            logging.error(f"FAILED check. {message}")
            self.checks_failed += 1
            if raise_exception:
                raise AssertionError(f"FAILED check. {message}")

    def check_quiet(self, cond, message="", raise_exception=False):
        if cond:
            logging.debug(f"PASSED check. {message}")
            self.checks_passed += 1
        else:
            logging.error(f"FAILED check. {message}")
            self.checks_failed += 1
            if raise_exception:
                raise AssertionError(f"FAILED check. {message}")

    def report_log(self, message=""):
        logging.info(f"{message}: {self.checks_passed} checks passed, {self.checks_failed} checks failed.")

    def report_print(self, message=""):
        print(f"{message}: {self.checks_passed} checks passed, {self.checks_failed} checks failed.")

class Date:

    def log_timestamp(self):    
        ts_UTC = int(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())
        logging.info(f"Current time: {datetime.fromtimestamp(ts_UTC)} = {ts_UTC} seconds")
