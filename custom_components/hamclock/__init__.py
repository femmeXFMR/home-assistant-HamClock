"""Home Assistant HamClock Integration."""
import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the HamClock integration."""
    _LOGGER.info("HamClock integration loaded")
    return True
