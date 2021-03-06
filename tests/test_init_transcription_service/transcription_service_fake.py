from typing import Any, Callable, Dict, Iterable, Optional
from transcribe import (
    register_transcription_service_factory,
    TranscribeBatchResult,
    TranscribeJobRequest,
    TranscribeJobsUpdate,
    TranscriptionService,
)
from unittest.mock import Mock


class FakeTranscriptionService(TranscriptionService):
    def __init__(self, config: Dict[str, Any] = {}, **kwargs):
        self._init_service_mock = Mock()
        self._transcribe_mock = Mock()

    def get_init_service_mock(self) -> Mock:
        return self._init_service_mock

    def get_transcribe_mock(self) -> Mock:
        return self._transcribe_mock

    def init_service(self, config: Dict[str, Any] = {}, **kwargs) -> None:
        self._init_service_mock(config)

    def transcribe(
        self,
        transcribe_requests: Iterable[TranscribeJobRequest],
        batch_id: str = "",
        on_update: Optional[Callable[[TranscribeJobsUpdate], None]] = None,
        **kwargs,
    ) -> TranscribeBatchResult:
        return self._transcribe_mock(
            transcribe_requests,
            batch_id=batch_id,
            poll_interval=kwargs.get("poll_interval", 5),
            on_update=on_update,
        )


def __factory() -> TranscriptionService:
    return FakeTranscriptionService()


register_transcription_service_factory(
    "tests.test_init_transcription_service.transcription_service_fake", __factory
)
