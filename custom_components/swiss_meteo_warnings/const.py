"""Constants for swiss_meteo_warnings."""
from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

NAME = "Swiss Meteo Warnings"
DOMAIN = "swiss_meteo_warnings"
VERSION = "1.0.0"
ATTRIBUTION = "Data provided by Meteo Swiss"

CONF_PLACE = "place"
CONF_POST_CODE = "post_code"
