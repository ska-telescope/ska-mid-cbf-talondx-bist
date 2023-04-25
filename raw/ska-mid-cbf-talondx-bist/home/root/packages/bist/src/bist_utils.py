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

class influx_csv:

    def __init__(self, file_name):
        self.file_name = file_name
        """
        append a new line at begining of the file on object initialization
        influx does not have an issue with having multiple empty lines
        between each csv block, but it does need a minimum of one
        """
        with open(file_name, "a" ) as file_ds:
            file_ds.write('\r\n')

    def __write_list_delimiter__(self, file_ds, data_list, delimiter=','):
        for idx, cell in enumerate(data_list):
            s=str(cell) # explicitly convert to string
            file_ds.write(s)
            if idx != len(data_list)-1:
                file_ds.write(delimiter)
        #insert a newline at the end
        file_ds.write('\n')

    def write_datatype(self, datatype_list):
        with open(self.file_name, "a" ) as file_ds:
            file_ds.write("#datatype ")
            self.__write_list_delimiter__(file_ds, datatype_list)
    
    def write_header(self, header_list):
        with open(self.file_name, "a" ) as file_ds:
            self.__write_list_delimiter__(file_ds, header_list)

    def write_csv(self, data_row, time=None):
        if time is not None:
            timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ") # convert to RFC3339 timestamp
            data_row.append(timestamp)

        with open( self.file_name, "a" ) as file_ds:
            self.__write_list_delimiter__(file_ds, data_row)