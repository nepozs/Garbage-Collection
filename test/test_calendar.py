"""Test all frequencies (except blank)."""

from datetime import datetime

from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.garbage_collection import const


async def test_calendar(hass: HomeAssistant) -> None:
    """Weekly collection."""

    config_entry: MockConfigEntry = MockConfigEntry(
        domain=const.DOMAIN,
        options={"frequency": "weekly", "collection_days": ["mon"]},
        title="calendar",
        version=6,
    )
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    calendar = hass.states.get("calendar.garbage_collection")
    assert calendar is not None
    assert calendar.attributes["message"] == "calendar"
    assert calendar.state == "off"
    start_time = calendar.attributes["start_time"]
    end_time = calendar.attributes["end_time"]
    assert start_time == "2020-04-06 00:00:00"
    assert end_time == "2020-04-07 00:00:00"
    start_date = datetime(2020, 4, 1)
    end_date = datetime(2020, 5, 1)
    events = await hass.data["garbage_collection"]["calendar"].async_get_events(
        hass, start_date, end_date
    )
    assert len(events) == 4
