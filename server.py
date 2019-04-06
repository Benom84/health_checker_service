import json
import logging

from flask import Flask
from health_checkers.activate_health_checks import HealthCheckersActivator

app = Flask(__name__)
logger = logging.getLogger(__name__)


@app.route("/health_status")
def health_status():
    results = {"status": "error", "data": {}}
    try:
        health_checker_activator = HealthCheckersActivator()
        health_checkers = health_checker_activator.get_health_checkers_dict()
        results["data"] = {"overallHealth": dict()}
        for site, health_checker in health_checkers.items():
            results["data"]["overallHealth"][site] = "Good" if health_checker.check_health() else "Bad"
        results["status"] = "success"
    except:
        logger.exception("Error occurred while getting health_status")
    finally:
        return json.dumps(results)


@app.route("/availability")
def availability():
    results = {"status": "error", "data": {}}
    try:
        health_checker_activator = HealthCheckersActivator()
        health_checkers = health_checker_activator.get_health_checkers_dict()
        results["data"] = {"availabilityLastHour": dict()}
        for site, health_checker in health_checkers.items():
            results["data"]["availabilityLastHour"][site] = health_checker.get_health_check_statistics()
        results["status"] = "success"
    except:
        logger.exception("Error occurred while getting availability")
    finally:
        return json.dumps(results)


def start_health_checkers():
    health_checker_activator = HealthCheckersActivator()
    health_checker_activator.activate_health_checkers_schedule()


def run_server():
    start_health_checkers()
    app.run(debug=True, use_reloader=False)


if __name__ == '__main__':
    run_server()
