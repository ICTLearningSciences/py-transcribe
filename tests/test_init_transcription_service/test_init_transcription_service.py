from imp import reload
import os

import pytest

import transcribe


@pytest.fixture(autouse=True)
def before_each_reset_modules_and_env():
    reload(os)
    reload(transcribe)
    if "TRANSCRIBE_MODULE_PATH" in os.environ:
        del os.environ["TRANSCRIBE_MODULE_PATH"]
    yield


def test_it_creates_a_service_configured_by_env():
    os.environ["TRANSCRIBE_MODULE_PATH"] = "tests.test_init_transcription_service.transcription_service_fake"
    service = transcribe.init_transcription_service()
    assert isinstance(service, transcribe.TranscriptionService)
    service.get_init_service_mock().assert_called_once()


def test_it_raises_error_when_no_service_configured():
    ex_caught: EnvironmentError = None
    try:
        transcribe.init_transcription_service()
    except EnvironmentError as ex:
        ex_caught = ex
    assert isinstance(ex_caught, EnvironmentError)
    assert str(ex_caught) == "missing required env 'TRANSCRIBE_MODULE_PATH' which should point to a TransciptionService implementation."


def test_it_raises_when_registered_module_path_not_found():
    os.environ["TRANSCRIBE_MODULE_PATH"] = "tests.module_does_not_exists"
    ex_caught: ModuleNotFoundError = None
    try:
        transcribe.init_transcription_service()
    except ModuleNotFoundError as ex:
        ex_caught = ex
    assert isinstance(ex_caught, ModuleNotFoundError)


def test_it_raises_error_configured_module_path_fails_to_register_a_service_factory():
    os.environ["TRANSCRIBE_MODULE_PATH"] = "tests.test_init_transcription_service.transcription_service_fails_to_register"
    ex_caught: RuntimeError = None
    try:
        transcribe.init_transcription_service()
    except RuntimeError as ex:
        ex_caught = ex
    assert isinstance(ex_caught, RuntimeError)
    assert str(ex_caught) == "Module found for path tests.test_init_transcription_service.transcription_service_fails_to_register but no registered TranscriptionService factory. Perhaps the module is not calling register_transcription_service_factory from __init__.py?"
