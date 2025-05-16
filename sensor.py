import logging
import re
import requests
from urllib.parse import urlparse

import voluptuous as vol
from homeassistant.components.sensor import SensorEntity

from .const import CONF_PRODUCT_URL, CONF_REGION, CONF_NAME

_LOGGER = logging.getLogger(__name__)

def get_shopify_api_url(product_url):
    """
    Generate the Shopify API URL from the given product URL.
    Extract the product handle and build a URL in the format:
      https://<domain>/products/<handle>.json
    """
    match = re.search(r'/products/([^/?]+)', product_url)
    if match:
        handle = match.group(1)
        parsed = urlparse(product_url)
        return f"{parsed.scheme}://{parsed.netloc}/products/{handle}.json"
    return None

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the sensor from a config entry."""
    product_url = entry.data[CONF_PRODUCT_URL]
    region = entry.data[CONF_REGION]
    name = entry.data.get(CONF_NAME, "")
    async_add_entities([UnifiStockSensor(name, product_url, region, entry)], True)

class UnifiStockSensor(SensorEntity):
    """Representation of a Ubiquiti product stock sensor using a mixed approach."""

    def __init__(self, name, product_url, region, entry):
        """Initialize the sensor."""
        self._name = name
        self._product_url = product_url
        self._region = region
        self._state = None
        self._available = True
        self._attr_icon = "mdi:checkbox-marked-circle-outline"
        self._attr_unique_id = entry.entry_id
        self.entry_id = entry.entry_id

    @property
    def name(self):
        """Return the sensor name."""
        return self._name

    @property
    def state(self):
        """Return the sensor state."""
        return self._state

    @property
    def available(self):
        """Return if the sensor is available."""
        return self._available

    def update(self):
        """
        Fetch the latest stock data using both the Shopify API and HTML scraping.
        First, try using the Shopify API by constructing the proper endpoint.
        If that fails, fall back to scraping the product page.
        """
        # --- Attempt Shopify API ---
        shopify_api_url = get_shopify_api_url(self._product_url)
        if shopify_api_url:
            try:
                response = requests.get(shopify_api_url, timeout=10)
                if response.status_code == 200:
                    json_data = response.json()
                    in_stock = False
                    variants = json_data.get("product", {}).get("variants", [])
                    for variant in variants:
                        if variant.get("available", False) or variant.get("inventory_quantity", 0) > 0:
                            in_stock = True
                            break
                    self._state = "In Stock" if in_stock else "Out of Stock"
                    self._available = True
                    return  # Successfully updated from API.
                else:
                    _LOGGER.warning("Shopify API URL returned status code %s", response.status_code)
            except Exception as api_error:
                _LOGGER.warning("Shopify API method failed: %s", api_error)

        # --- Fallback: HTML scraping ---
        try:
            response = requests.get(self._product_url, timeout=10)
            response.raise_for_status()
            page_text = response.text.lower()
            if "add to cart" in page_text and "sold out" not in page_text:
                self._state = "In Stock"
            else:
                self._state = "Out of Stock"
            self._available = True
        except Exception as scrape_error:
            _LOGGER.warning("Scraping method failed: %s", scrape_error)
            self._available = False
            self._state = None
