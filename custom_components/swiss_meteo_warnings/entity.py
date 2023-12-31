"""SwissMeteoWarningsEntity class."""
from __future__ import annotations

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, LOGGER, DOMAIN, NAME, VERSION
from .coordinator import SwissMeteoWarningsCoordinator


class SwissMeteoWarningsEntity(CoordinatorEntity):
    """SwissMeteoWarningsEntity class."""

    LOGGER.debug("Swiss Meteo Warnings - entity")

    _attr_attribution = ATTRIBUTION

    def __init__(self, coordinator: SwissMeteoWarningsCoordinator) -> None:
        """Initialize."""
        LOGGER.debug("Swiss Meteo Warnings - entity - __init__")
        super().__init__(coordinator)
        self._attr_unique_id = coordinator.config_entry.entry_id
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.unique_id)},
            name=NAME,
            model=VERSION,
            manufacturer=NAME,
        )
