"""Adds config flow for Blueprint."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .geodata import GeoData

from .const import DOMAIN, LOGGER, CONF_POST_CODE, CONF_PLACE

class SwissMeteoWarningsFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Swiss Meteo Warnings."""

    LOGGER.debug("Swiss Meteo Warnings - config flow - SwissMeteoWarningsFlowHandler")

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            return self.async_create_entry(
                title=user_input[CONF_PLACE],
                data=user_input,
            )

        LOGGER.debug("Swiss Meteo Warnings - config flow - get geo data")
        geo_data = GeoData(
            self.hass.config.latitude,
            self.hass.config.longitude,
            session=async_get_clientsession(self.hass)
        )
        await geo_data.init_geo_data()
        place = geo_data.get_place()
        post_code = geo_data.get_post_code()

        LOGGER.debug("Swiss Meteo Warnings - config flow - got geo data")

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_POST_CODE,
                        default=post_code,
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT
                        ),
                    ),
                    vol.Required(
                        CONF_PLACE,
                        default=place,
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT
                        ),
                    ),
                }
            ),
            errors=_errors,
        )
