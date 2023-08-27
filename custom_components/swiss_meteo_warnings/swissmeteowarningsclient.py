''' Swiss Meteo Api Client '''
import json
import logging

from datetime import datetime
from enum import IntEnum

import requests  # type: ignore
import pandas as pd


_LOGGER = logging.getLogger(__name__)

JSON_FORECAST_URL = "https://app-prod-ws.meteoswiss-app.ch/v2/plzDetail?plz={}00"

class WarningType(IntEnum):
    """ Types of warnings with ids """
    THUNDERSTORM = 1
    RAIN = 2
    HEAT_WAVE = 7
    FOREST_FIRE = 10
    FLOOD = 11
    '''
    AVALANCHES =
    EARTHQUAKE =
    FROST =
    SLIPPERY_ROADS =
    SNOW =
    WIND =
    '''
    UNKNOWN = 1000

class WarningLevel(IntEnum):
    """ Warnings level definitions """
    NONE = 0
    LOW = 1
    MODERATE = 2
    CONSIDERABLE = 3
    HIGH = 4
    HIGHEST = 5

class Link():
    """ Link returned by Api """
    def __init__(self):
        self.text = None
        self.url = None

    text: str
    url: str

class SwissMeteoWarning():
    """ Warning object definition """
    def __init__(self):
        self.text = None
        self.html = None
        self.valid_from = datetime.min
        self.valid_to = datetime.max
        self.links = list[Link]()

    text: str
    html: str
    type: WarningType
    level: WarningLevel
    outlook: bool
    valid_from: datetime.timestamp
    validTo: datetime.timestamp
    links: list[Link]


class SwissMeteoWarningsClient:
    """ Client for meteo swiss """
    def __init__(self, display_name=None, post_code=None, language=None, country=None):
        _LOGGER.debug("Meteo Swiss Warnings Client INIT")
        self.__post_code = post_code
        self.__name = display_name
        self.__warnings = None

        accept_language = ""
        if (language is not None and country is not None):
            accept_language = language + "," + language + "-" + country + ";"
        elif language is not None:
            accept_language = language + ";"

        self.__headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": accept_language + "q=0.8,en-US;q=0.5,en;q=0.3",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/1337 Safari/537.36",
        }

        _LOGGER.debug(
            "Meteo Swiss Warnings client with : name = %s postcode = %s language = %s",
            self.__name, self.__post_code, accept_language
        )

    def get_typed_data(self) -> list[SwissMeteoWarning]:
        """ Get typed object """
        if self.__warnings is None:
            return None
        else:
            warnings = list[SwissMeteoWarning]()
            for json_warning in self.__warnings:
                if 'warnLevel' in json_warning:
                    warn_level_int = json_warning.get('warnLevel')
                    try:
                        warn_level = WarningLevel(warn_level_int)
                        if (warn_level is WarningLevel.NONE or warn_level is WarningLevel.LOW):
                            continue
                    except Exception:
                        _LOGGER.warning("Meteo Swiss Warnings Client - Warning level %s unknown.", str(warn_level_int))
                        warn_level = WarningLevel.NONE
                else:
                    continue

                if 'warnType' in json_warning:
                    warn_type_int = json_warning.get('warnType')
                    try:
                        warn_type = WarningType(warn_type_int)
                    except Exception:
                        _LOGGER.warning("Meteo Swiss Warnings Client - Warning type %s unknown.", str(warn_type_int))
                        warn_type = WarningType.UNKNOWN
                else:
                    continue

                warning = SwissMeteoWarning()
                warning.type = warn_type
                warning.level = warn_level

                warning.text = json_warning.get('text')
                warning.html = json_warning.get('htmlText')

                warning.outlook = json_warning.get('outlook')
                if warning.outlook is None:
                    warning.outlook = False

                if 'validFrom' in json_warning:
                    warning.valid_from = pd.to_datetime(json_warning['validFrom'], unit="ms")
                if 'validTo' in json_warning:
                    warning.valid_to = pd.to_datetime(json_warning['validTo'], unit="ms")

                if 'links' in json_warning:
                    for json_link in json_warning['links']:
                        link = Link()
                        link.url = json_link.get('url')
                        link.text = json_link.get('text')
                        warning.links.append(link)

                warnings.append(warning)
            return warnings

    def __get_warnings(self):
        json_url = JSON_FORECAST_URL.format(self.__post_code)
        _LOGGER.debug("Start update warnings data")
        request = requests.Session()
        request.headers.update(self.__headers)
        response = request.get(json_url, timeout=10)
        if response.ok:
            self.__warnings = json.loads(response.text)['warnings']
        else:
            _LOGGER.warning("Meteo Swiss Warnings Client - Request error : %s", str(response.status_code))
            self.__warnings = None
        _LOGGER.debug("End of warnings udate")

    def update(self):
        self.__get_warnings()
