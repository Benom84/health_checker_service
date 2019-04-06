import atexit
import logging
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from singleton_decorator import singleton

from health_checkers.health_checker import HealthChecker
from health_checkers.health_checkers_configuration import HEALTH_CHECKERS_CONFIGURATION_DICT
from health_checkers.health_checkers_constants import INTERVAL_BETWEEN_HEALTH_CHECK_IN_SECONDS

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logging.getLogger('apscheduler').setLevel(logging.WARNING)


@singleton
class HealthCheckersActivator:
    def __init__(self):
        self.__health_checks = dict()
        self.scheduler = None

    def get_health_checkers_dict(self):
        return dict(self.__health_checks)

    def activate_health_checkers_schedule(self):

        self.__create_health_checkers()
        self.__schedule_health_checkers(self.__health_checks)

    def __schedule_health_checkers(self, all_health_checks):
        self.scheduler = BackgroundScheduler()
        for hc in all_health_checks.values():
            self.scheduler.add_job(func=hc.update_health_check_statistics,
                                   trigger="interval",
                                   seconds=INTERVAL_BETWEEN_HEALTH_CHECK_IN_SECONDS,
                                   next_run_time=datetime.now())
        self.scheduler.start()
        atexit.register(lambda: self.scheduler.shutdown())

    def __create_health_checkers(self):
        all_health_checks = {}
        for target, config in HEALTH_CHECKERS_CONFIGURATION_DICT.items():
            all_health_checks[target] = HealthChecker(target, config["parser"](), config["data_fetcher"], logger)
        self.__health_checks = all_health_checks
