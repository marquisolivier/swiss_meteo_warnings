"""Definition of Swiss Meteo Warning sensor platform."""
from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, LOGGER
from .swissmeteowarningsclient import SwissMeteoWarning, WarningType, WarningLevel

from .coordinator import SwissMeteoWarningsCoordinator

@dataclass
class SwissMeteoWarningsEntityDescription(SensorEntityDescription):
    """Describes Swiss Meteo Warning sensor entity."""

# Keys must match those in the data dictionary
SENSOR_TYPES: list[SwissMeteoWarningsEntityDescription] = [
    SwissMeteoWarningsEntityDescription(
        key=WarningType.THUNDERSTORM,
        translation_key="thunderstorm",
        state_class=SensorStateClass.MEASUREMENT,
        #value=lambda data: LOGGER.warn(data),
        icon="mdi:weather-lightning",
    ),
    SwissMeteoWarningsEntityDescription(
        key=WarningType.RAIN,
        translation_key="rain",
        state_class=SensorStateClass.MEASUREMENT,
        #value=lambda data: data.get("nh3_MR100"),
        icon="mdi:weather-pouring",
    ),
    SwissMeteoWarningsEntityDescription(
        key=WarningType.HEAT_WAVE,
        translation_key="heat_wave",
        state_class=SensorStateClass.MEASUREMENT,
        #value=lambda data: data.get("ash3"),
        icon="mdi:heat-wave",
    ),
    SwissMeteoWarningsEntityDescription(
        key=WarningType.FOREST_FIRE,
        translation_key="forest_fire",
        state_class=SensorStateClass.MEASUREMENT,
        #value=lambda data: data.get("ash3"),
        icon="mdi:fire",
    ),
    SwissMeteoWarningsEntityDescription(
        key=WarningType.FLOOD,
        translation_key="flood",
        state_class=SensorStateClass.MEASUREMENT,
        #value=lambda data: data.get("ash3"),
        icon="mdi:home-flood",
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    config: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensor entities based on a config entry."""
    LOGGER.debug("Swiss Meteo Warnings - sensor - async_setup_entry")

    coordinator = hass.data[DOMAIN][config.entry_id]

    entities: list[SwissMeteoWarningSensor] = []

    for description in SENSOR_TYPES:
        entities.append(SwissMeteoWarningSensor(coordinator, description))

    async_add_entities(entities)


class SwissMeteoWarningSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Sensor."""

    LOGGER.debug("Swiss Meteo Warnings - sensor")
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: SwissMeteoWarningsCoordinator,
        description: SwissMeteoWarningsEntityDescription,
    ) -> None:
        """Initialize a single sensor."""
        LOGGER.debug("Swiss Meteo Warnings - sensor - __init__")
        super().__init__(coordinator)
        self.entity_description: SwissMeteoWarningsEntityDescription = description

        self._attr_device_info = coordinator.client.post_code
        self._attr_unique_id = f"{coordinator.client.post_code}_{description.key.name}"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        LOGGER.debug("Swiss Meteo Warnings - sensor - _handle_coordinator_update")
        warnings = list[SwissMeteoWarning](self.coordinator.data)

        warning_level = WarningLevel.NONE
        if len(warnings) > 0:
            warning = next((w for w in warnings if w.type is self.entity_description.key), None)
            if warning is not None:
                warning_level = warning.level

        LOGGER.debug("Swiss Meteo Warnings - sensor - level")
        self._attr_native_value = int(warning_level)
        LOGGER.debug("%s is %s (%s)", self.entity_description.key.name,
            warning_level.name,
            self._attr_native_value
        )
        
        self.async_write_ha_state()

