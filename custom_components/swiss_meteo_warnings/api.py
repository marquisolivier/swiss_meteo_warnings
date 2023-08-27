"""Swiss Meteo API Client."""
from __future__ import annotations

import asyncio
import socket

import aiohttp
import async_timeout


class SwissMeteoWarningsApiClientError(Exception):
    """Exception to indicate a general API error."""

class SwissMeteoWarningsApiClientCommunicationError(
    SwissMeteoWarningsApiClientError
):
    """Exception to indicate a communication error."""

class SwissMeteoWarningsApiClient:
    """Meteo Swiss Warnings API Client."""

    def __init__(
        self,
        post_code: int,
        place: str,
        language : str,
        country : str,
        session: aiohttp.ClientSession,
    ) -> None:
        """Meteo Swiss Warnings API Client."""
        self.__post_code = post_code
        self.__place = place
        self.__session = session
        accept_language = ""

        if (language is not None and country is not None):
            accept_language = language + "," + language + "-" + country + ";"
        elif (language is not None ):
            accept_language = language + ";"

        self.__headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": accept_language + "q=0.8,en-US;q=0.5,en;q=0.3",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/1337 Safari/537.36",
        }


    async def async_get_data(self) -> any:
        """Get data from the API."""
        #self.__warnings = json.loads(response.text)['warnings']
        return await self._api_wrapper(
            method="get",
            url = f"https://app-prod-ws.meteoswiss-app.ch/v2/plzDetail?plz={self.__post_code}00",
            headers=self.__headers
        )

    async def async_set_title(self, value: str) -> any:
        """Get data from the API."""
        return await self._api_wrapper(
            method="patch",
            url="https://jsonplaceholder.typicode.com/posts/1",
            data={"title": value},
            headers={"Content-type": "application/json; charset=UTF-8"},
        )

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
