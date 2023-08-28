"""class to help to get post code and place."""

from __future__ import annotations

import aiohttp
import async_timeout

from .const import LOGGER

_HEADERS = {
    "Accept":
       "application/json",
    "Accept-Encoding":
       "gzip, deflate, sdch",
    "User-Agent":
       "Mozilla/5.0 (X11; Linux x86_64) " +
       "AppleWebKit/537.36 (KHTML, like Gecko) " +
       "Chrome/1337 " +
       "Safari/537.36",
}

_API_URL = "https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={}&lon={}"

class GeoData:
    """Geo Data API Client."""

    def __init__(
        self,
        latitude : float,
        longitude : float,
        session : aiohttp.ClientSession,
    ) -> None:
        """Init class."""
        self.__address = None
        self.__latitude = latitude
        self.__longitude = longitude
        self.__session = session

    async def init_geo_data(self):
        """Init geo data."""
        self.__address = None

        url = _API_URL.format(self.__latitude, self.__longitude)
        LOGGER.info(url)
        async with async_timeout.timeout(10):
            response = await self.__session.request(
                method="get",
                url=url,
                headers=_HEADERS,
                json="",
            )
            response.raise_for_status()
            self.__address = (await response.json()).get("address")

    def get_place(self):
        """Get the place associated with the address."""
        if self.__address is None:
            return None

        interests = ["village", "town", "suburb", "city", "quartier", "municipality", "county"]
        for interest in interests:
            if interest in self.__address:
                return self.__address[interest]

        return None

    def get_post_code(self):
        """Get the post code associated with the address."""
        if self.__address is None:
            return None

        return self.__address.get('postcode')
