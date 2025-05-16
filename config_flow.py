import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN, CONF_PRODUCT_URL, CONF_REGION, CONF_NAME

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_PRODUCT_URL): str,
    vol.Optional(CONF_REGION, default="us"): str,
    vol.Optional(CONF_NAME, default=""): str,
})

class UnifiStockConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for the UniFi Stock Check integration."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            product_url = user_input[CONF_PRODUCT_URL]
            if not product_url.startswith("http"):
                errors["base"] = "invalid_url"
            elif "/products/" not in product_url:
                errors["base"] = "invalid_product_url"
            if not errors:
                return self.async_create_entry(title=user_input.get(CONF_NAME), data=user_input)
        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA, errors=errors)
