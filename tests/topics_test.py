# Copyright (c) 2025 csg-sa

from types import MappingProxyType

import pytest

from greencell_client import topics


def test_valid_topics_returned_and_immutable():
    serial = "EVSE123"
    test_topics = topics.get_mqtt_topics(serial)

    assert isinstance(test_topics, MappingProxyType)
    assert test_topics["current"] == f"{topics.MQTT_TOPIC_BASE}/{serial}/current"
    assert test_topics["voltage"] == f"{topics.MQTT_TOPIC_BASE}/{serial}/voltage"
    assert test_topics["power"] == f"{topics.MQTT_TOPIC_BASE}/{serial}/power"
    assert test_topics["status"] == f"{topics.MQTT_TOPIC_BASE}/{serial}/status"
    assert test_topics["device_state"] == f"{topics.MQTT_TOPIC_BASE}/{serial}/device_state"

    # MappingProxyType is immutable
    with pytest.raises(TypeError):
        test_topics["new"] = "value"


def test_caching_behavior(monkeypatch):
    serial = "CACHE123"

    # Ensure function is called only once by patching MappingProxyType
    call_count = {}

    def fake_proxy(arg):
        call_count["calls"] = call_count.get("calls", 0) + 1
        return MappingProxyType(arg)

    monkeypatch.setattr(topics, "MappingProxyType", fake_proxy)

    result1 = topics.get_mqtt_topics(serial)
    result2 = topics.get_mqtt_topics(serial)

    assert result1 == result2
    assert call_count["calls"] == 1  # lru_cache worked


@pytest.mark.parametrize("bad_value", [None, 123, 12.34, object()])
def test_invalid_type_raises(bad_value):
    with pytest.raises(ValueError, match="not a string"):
        topics.get_mqtt_topics(bad_value)  # type: ignore[arg-type]


@pytest.mark.parametrize("bad_value", ["", "   "])
def test_empty_or_whitespace_serial_raises(bad_value):
    with pytest.raises(ValueError, match="empty/whitespace"):
        topics.get_mqtt_topics(bad_value)


@pytest.mark.parametrize("bad_value", ["bad serial", "EVSE#", "EVSE+"])
def test_invalid_characters_raise(bad_value):
    with pytest.raises(ValueError, match="Invalid serial number for MQTT topic"):
        topics.get_mqtt_topics(bad_value)
