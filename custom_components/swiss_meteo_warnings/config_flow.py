"""Adds config flow for Blueprint."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .geodata import GeoData

from .const import CONF_POST_CODE, CONF_PLACE
from .const import DOMAIN

class SwissMeteoWarningsFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Swiss Meteo Warnings."""

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

        geoData = GeoData(
            self.hass.config.latitude,
            self.hass.config.longitude,
            session=async_get_clientsession(self.hass)
        )
        await geoData.init_geo_data()
        place = geoData.get_place()
        post_code = geoData.get_post_code()

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