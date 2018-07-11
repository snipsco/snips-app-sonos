from collections import defaultdict
import pytest
import mock

hermes_python = pytest.importorskip("hermes-python")



from snipssonos.shared.request_object import ValidRequestObject, InvalidRequestObject
from snipssonos.use_cases.request_objects import VolumeSetRequestObject
from snipssonos.adapters.request_adapter import VolumeSetRequestAdapter


def generate_volume_slot(volume_increase):
    volume_slot_value = mock.create_autospec(hermes_python.ontology.SlotValue)
    volume_slot_value.value = hermes_python.ontology.NumberValue(volume_increase)
    volume_slot = mock.create_autospec(hermes_python.ontology.Slot)
    volume_slot.slot_value = volume_slot_value

    return volume_slot


@pytest.fixture
def correct_intent_message():
    VOLUME_INCREASE = 10
    volume_slot = generate_volume_slot(VOLUME_INCREASE)

    slots_mapping = defaultdict(hermes_python.ontology.SlotsList)
    slots_mapping['volume_set_percentage'] = hermes_python.ontology.SlotsList([volume_slot])
    slots = hermes_python.ontology.SlotMap(slots_mapping)

    intent_message = hermes_python.ontology.IntentMessage(
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

    slots_mapping = defaultdict(hermes_python.ontology.SlotsList)
    slots_mapping['volume_set_absolute'] = hermes_python.ontology.SlotsList([first_volume_slot, second_volume_slot])
    slots = hermes_python.ontology.SlotMap(slots_mapping)

    intent_message = hermes_python.ontology.IntentMessage(
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
    slots_mapping = defaultdict(hermes_python.ontology.SlotsList)
    slots = hermes_python.ontology.SlotMap(slots_mapping)

    empty_intent_message = hermes_python.ontology.IntentMessage(
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

    fake_slot_value = mock.create_autospec(hermes_python.ontology.SlotValue)
    fake_slot_value.value = hermes_python.ontology.NumberValue(9000)
    fake_slot = mock.create_autospec(hermes_python.ontology.Slot)
    fake_slot.slot_value = fake_slot_value

    slots_mapping = defaultdict(hermes_python.ontology.SlotsList)
    slots_mapping['volume_set_absolute'] = hermes_python.ontology.SlotsList([volume_slot])
    slots_mapping['fake_slot'] = hermes_python.ontology.SlotsList([fake_slot])

    slots = hermes_python.ontology.SlotMap(slots_mapping)

    intent_message = hermes_python.ontology.IntentMessage(
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
