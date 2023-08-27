"""Custom integration to integrate swiss_meteo_warnings with Home Assistant.

For more details about this integration, please refer to
https://github.com/marquisolivier/swiss_meteo_warnings
"""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .swissmeteowarningsclient import SwissMeteoWarningsApiClient
from .const import DOMAIN, CONF_POST_CODE
from .coordinator import SwissMeteoWarningsCoordinator

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
]

# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up this integration using UI."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][
        entry.entry_id
    ] = coordinator = SwissMeteoWarningsCoordinator(
        hass=hass,
        client=SwissMeteoWarningsApiClient(
            entry.data[CONF_POST_CODE],
            hass.config.language,
            hass.config.country,
            session=async_get_clientsession(hass),
        )
    )

    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    if unloaded := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
