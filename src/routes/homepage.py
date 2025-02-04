import datetime
from flask import render_template, blueprints

from src.config import app
from src.models import SpeedTestResult, DashboardSettings, SystemInfo
from src.utils import datetimeformat, get_system_info

homepage_bp = blueprints.Blueprint("homepage", __name__)

@app.route("/")
def dashboard():
    settings = DashboardSettings.query.first()
    SPEEDTEST_COOLDOWN_IN_HOURS = settings.speedtest_cooldown
    system_info = get_system_info()

    # Fetch the last speedtest result
    n_hour_ago = datetime.datetime.now() - datetime.timedelta(
        hours=SPEEDTEST_COOLDOWN_IN_HOURS)
    recent_results = SpeedTestResult.query.filter(
        SpeedTestResult.timestamp > n_hour_ago).all()
    last_timestamp = (
        datetimeformat(recent_results[-1].timestamp) if recent_results else None
    )

    if recent_results:
        # Display the most recent result from the database
        latest_result = recent_results[-1]
        speedtest_result = {
            "download_speed": latest_result.download_speed,
            "upload_speed": latest_result.upload_speed,
            "ping": latest_result.ping,
        }
        source = "Database"
        next_test_time = latest_result.timestamp + datetime.timedelta(
            hours=SPEEDTEST_COOLDOWN_IN_HOURS
        )
        show_prompt = False
        remaining_time_for_next_test = round(
            (next_test_time - datetime.datetime.now()).total_seconds() / 60
        )
    else:
        # No recent results, prompt to perform a test
        speedtest_result = None
        source = None
        show_prompt = True
        remaining_time_for_next_test = None

    return render_template(
        "dashboard.html",
        system_info=system_info,
        speedtest_result=speedtest_result,
        source=source,
        last_timestamp=last_timestamp,
        next_test_time=remaining_time_for_next_test,
        show_prompt=show_prompt,
    )
