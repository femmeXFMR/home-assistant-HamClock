"""Constants for the HamClock integration."""

DOMAIN = "hamclock"
NAME = "HamClock"
VERSION = "1.0.0"
ISSUE_URL = "https://github.com/femmeXFMR/home-assistant-HamClock/issues"

# Configuration
CONF_UPDATE_INTERVAL = "update_interval"
CONF_KP_ALERT_THRESHOLD = "kp_alert_threshold"
CONF_XRAY_ALERT_THRESHOLD = "xray_alert_threshold"
CONF_ENABLE_ALERTS = "enable_alerts"

# Default values
DEFAULT_UPDATE_INTERVAL = 900  # 15 minutes
DEFAULT_KP_ALERT_THRESHOLD = 6.0
DEFAULT_XRAY_ALERT_THRESHOLD = "M"
DEFAULT_ENABLE_ALERTS = True
