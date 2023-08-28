"""Swiss Meteo API Client."""
from __future__ import annotations

import asyncio
import socket
from enum import IntEnum
from datetime import datetime
import aiohttp
import async_timeout

import pandas as pd

from .const import LOGGER

class WarningType(IntEnum):
    """Types of warnings with ids."""

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
    """Warnings level definitions."""

    NONE = 0
    LOW = 1
    MODERATE = 2
    CONSIDERABLE = 3
    HIGH = 4
    HIGHEST = 5

class Link():
    """Link returned by Api."""

    def __init__(self):
        """Init class."""
        self.text = None
        self.url = None

    text: str
    url: str

class SwissMeteoWarning():
    """Warning object definition."""

    def __init__(self):
        """Init class."""
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



class SwissMeteoWarningsApiClientError(Exception):
    """Exception to indicate a general API error."""

class SwissMeteoWarningsApiClientCommunicationError(
    SwissMeteoWarningsApiClientError
):
    """Exception to indicate a communication error."""

class SwissMeteoWarningsApiClient:
    """Meteo Swiss Warnings API Client."""

    LOGGER.info("Create SwissMeteoWarningsApiClient instance")

    def __init__(
        self,
        post_code: int,
        language : str,
        country : str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Meteo Swiss Warnings API Client."""
        self.post_code = post_code
        self.__session = session
        accept_language = language

        LOGGER.debug("Init SwissMeteoWarningsApiClient with %s and %s", self.post_code, self.__session)

        if (language is not None and country is not None):
            accept_language = language + "," + language + "-" + country + ";"
        elif language is not None:
            accept_language = language + ";"

        self.__headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": accept_language + "q=0.8,en-US;q=0.5,en;q=0.3",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) " +
                          "AppleWebKit/537.36 (KHTML, like Gecko)" +
                          "Chrome/1337 Safari/537.36",
        }


    async def async_get_data(self) -> any:
        """Get data from the API."""
        LOGGER.debug("Get data from SwissMeteoWarningsApiClient from the API")
        data = await self._api_wrapper(
            method="get",
            url = f"https://app-prod-ws.meteoswiss-app.ch/v2/plzDetail?plz={self.post_code}00",
            headers=self.__headers
        )

        warnings = list[SwissMeteoWarning]()
        for json_warning in data['warnings']:
            if 'warnLevel' in json_warning:
                warn_level_int = json_warning.get('warnLevel')
                try:
                    warn_level = WarningLevel(warn_level_int)
                    if (warn_level is WarningLevel.NONE or warn_level is WarningLevel.LOW):
                        continue
                except Exception:
                    LOGGER.warning("Meteo Swiss Warnings Client - Warning level %s unknown.", str(warn_level_int))
                    warn_level = WarningLevel.NONE
            else:
                continue

            if 'warnType' in json_warning:
                warn_type_int = json_warning.get('warnType')
                try:
                    warn_type = WarningType(warn_type_int)
                except Exception:
                    LOGGER.warning("Meteo Swiss Warnings Client - Warning type %s unknown.", str(warn_type_int))
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

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> any:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                response = await self.__session.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=data,
                )
                if response.status == 500:
                    raise SwissMeteoWarningsApiClientCommunicationError(
                        "Error 500. Probably unknown post code.",
                    )
                response.raise_for_status()
                return await response.json()

        except asyncio.TimeoutError as exception:
            raise SwissMeteoWarningsApiClientCommunicationError(
                "Timeout error fetching information",
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise SwissMeteoWarningsApiClientCommunicationError(
                "Error fetching information",
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            raise SwissMeteoWarningsApiClientError(
                "Something really wrong happened!"
            ) from exception
