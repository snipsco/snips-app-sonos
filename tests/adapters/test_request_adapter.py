from collections import defaultdict
import pytest
import mock

from hermes_python.ontology import IntentMessage, SlotMap, Slot, SlotValue, SlotsList, NumberValue

from snipssonos.shared.request_object import ValidRequestObject, InvalidRequestObject
from snipssonos.use_cases.request_objects import VolumeSetRequestObject
from snipssonos.adapters.request_adapter import VolumeSetRequestAdapter


def generate_volume_slot(volume_increase):
    volume_slot_value = mock.create_autospec(SlotValue)
    volume_slot_value.value = NumberValue(volume_increase)
    volume_slot = mock.create_autospec(Slot)
    volume_slot.slot_value = volume_slot_value

    return volume_slot


@pytest.fixture
def correct_intent_message():
    VOLUME_INCREASE = 10
    volume_slot = generate_volume_slot(VOLUME_INCREASE)

    slots_mapping = defaultdict(SlotsList)
    slots_mapping['volume_set_percentage'] = SlotsList([volume_slot])
    slots = SlotMap(slots_mapping)

    intent_message = IntentMessage(
        "session_id",
        "custom_data",
        "site_id",
        "input",
        "intent",
        slots
    )

    return intent_message


@pytest.fixture
def correct_intent_message_with_two_slots():
    VOLUME_INCREASE_FIRST = 10
    VOLUME_INCREASE_SECOND = 20

    first_volume_slot = generate_volume_slot(VOLUME_INCREASE_FIRST)
    second_volume_slot = generate_volume_slot(VOLUME_INCREASE_SECOND)

    slots_mapping = defaultdict(SlotsList)
    slots_mapping['volume_set_absolute'] = SlotsList([first_volume_slot, second_volume_slot])
    slots = SlotMap(slots_mapping)

    intent_message = IntentMessage(
        "session_id",
        "custom_data",
        "site_id",
        "input",
        "intent",
        slots
    )

    return intent_message


def test_volume_set_adapter_from_correct_intent_message_generates_valid_request(correct_intent_message):
    valid_request = VolumeSetRequestAdapter.from_intent_message(correct_intent_message)

    assert isinstance(valid_request, ValidRequestObject)
    assert isinstance(valid_request, VolumeSetRequestObject)


def test_volume_set_adapter_from_intent_message_with_no_slots_generates_invalid_request():
    slots_mapping = defaultdict(SlotsList)
    slots = SlotMap(slots_mapping)

    empty_intent_message = IntentMessage(
        "session_id",
        "custom_data",
        "site_id",
        "input",
        "intent",
        slots
    )

    valid_request = VolumeSetRequestAdapter.from_intent_message(empty_intent_message)

    assert isinstance(valid_request, InvalidRequestObject)


def test_volume_set_adapter_from_intent_message_with_multiple_slots_generates_valid_request():
    VOLUME_INCREASE = 10
    volume_slot = generate_volume_slot(VOLUME_INCREASE)

    fake_slot_value = mock.create_autospec(SlotValue)
    fake_slot_value.value = NumberValue(9000)
    fake_slot = mock.create_autospec(Slot)
    fake_slot.slot_value = fake_slot_value

    slots_mapping = defaultdict(SlotsList)
    slots_mapping['volume_set_absolute'] = SlotsList([volume_slot])
    slots_mapping['fake_slot'] = SlotsList([fake_slot])

    slots = SlotMap(slots_mapping)

    intent_message = IntentMessage(
        "session_id",
        "custom_data",
        "site_id",
        "input",
        "intent",
        slots
    )

    valid_request = VolumeSetRequestAdapter.from_intent_message(intent_message)

    assert isinstance(valid_request, ValidRequestObject)


def test_volume_set_adapter_from_intent_message_with_slot_with_array_of_values_generates_valid_request(
        correct_intent_message_with_two_slots):
    valid_request = VolumeSetRequestAdapter.from_intent_message(correct_intent_message_with_two_slots)

    assert isinstance(valid_request, ValidRequestObject)
    assert isinstance(valid_request, VolumeSetRequestObject)
