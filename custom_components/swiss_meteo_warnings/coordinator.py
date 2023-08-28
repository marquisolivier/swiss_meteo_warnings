"""DataUpdateCoordinator for swiss_meteo_warnings."""
from __future__ import annotations

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .swissmeteowarningsclient import (
    SwissMeteoWarningsApiClient,
    SwissMeteoWarningsApiClientError,
)

from .const import DOMAIN, LOGGER

class SwissMeteoWarningsCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    LOGGER.debug("Swiss Meteo Warnings - coordinator")

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        client: SwissMeteoWarningsApiClient,
    ) -> None:
        """Initialize."""
        LOGGER.debug("Swiss Meteo Warnings - coordinator - __init__")
        self.client = client
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(minutes=1),
        )

    async def _async_update_data(self):
        """Update data via library."""
        LOGGER.debug("Swiss Meteo Warnings - coordinator - _async_update_data")
        try:
            return await self.client.async_get_data()
        except SwissMeteoWarningsApiClientError as exception:
            raise UpdateFailed(exception) from exception
