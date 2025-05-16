"""UniFi Stock Check integration."""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

DOMAIN = "sl_unifi_stock"

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the UniFi Stock Check component."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up UniFi Stock Check from a config entry."""
    # hass.async_create_task(
    #    hass.config_entries.async_forward_entry_setup(entry, "sensor")
    # )
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload UniFi Stock Check config entry."""
    # unload_ok = await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    # return unload_ok
    await hass.config_entries.async_forward_entry_unload(entry, ["sensor"])
    return True

