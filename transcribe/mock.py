#
# This software is Copyright ©️ 2020 The University of Southern California. All Rights Reserved.
# Permission to use, copy, modify, and distribute this software and its documentation for educational, research and non-profit purposes, without fee, and without a written agreement is hereby granted, provided that the above copyright notice and subject to the full license file found in the root of this software deliverable. Permission to make commercial use of this software may be obtained by contacting:  USC Stevens Center for Innovation University of Southern California 1150 S. Olive Street, Suite 2300, Los Angeles, CA 90115, USA Email: accounting@stevens.usc.edu
#
# The full terms of this copyright and license should always be found in the root directory of this software deliverable as "license.txt" and if these terms are not found with this software, please contact the USC Stevens Center for the full license.
#
from dataclasses import dataclass, field
import os
from typing import Any, Callable, Dict, List, Optional
from unittest.mock import call, _Call, Mock


import yaml

try:
    from yaml import CLoader as YamlLoader
except ImportError:
    from yaml import Loader as YamlLoader  # type: ignore

from transcribe import (
    TranscribeBatchResult,
    TranscribeJob,
    TranscribeJobRequest,
    TranscribeJobStatus,
    TranscribeJobsUpdate,
)


def yaml_load(from_path: str) -> Dict[str, Any]:
    """
    Reads a dictionary from a given yaml file.
    Mainly broken out as a utility for convenience of mocking in tests,
    but also to handle in a single place the specific way
    that Loader must be imported and passed
    """
    with open(from_path, "r") as f:
        return yaml.load(f, Loader=YamlLoader)


@dataclass
class MockTranscribeJob:
    batch_id: str
    request: TranscribeJobRequest
    error: str = ""
    info: Dict[str, str] = field(default_factory=dict)
    status: TranscribeJobStatus = TranscribeJobStatus.SUCCEEDED
    transcript: str = ""

    def add_result(self, result: TranscribeBatchResult) -> TranscribeBatchResult:
        job = self.request.to_job(self.batch_id)
        result.transcribeJobsById[job.get_fq_id()] = job
        result.update_job(
            job.get_fq_id(),
            status=self.status,
            info=self.info,
            transcript=self.transcript,
            error=self.error,
        )
        return result


@dataclass
class MockTranscribeCallFixture:
    result: TranscribeBatchResult
    requests: List[TranscribeJobRequest] = field(default_factory=list)
    updates: List[TranscribeJobsUpdate] = field(default_factory=list)

    def __post_init__(self):
        self.requests = [
            TranscribeJobRequest(**i) if isinstance(i, dict) else i
            for i in self.requests
        ]
        if isinstance(self.result, dict):
            self.result = TranscribeBatchResult(
                transcribeJobsById={
                    k: v if isinstance(v, TranscribeJob) else TranscribeJob(**v)
                    for (k, v) in self.result["transcribeJobsById"].items()
                }
            )
        self.updates = [
            TranscribeJobsUpdate(**i) if isinstance(i, dict) else i
            for i in self.updates
        ]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "result": self.result.to_dict(),
            "requests": [i.to_dict() for i in self.requests],
            "updates": [i.to_dict() for i in self.updates],
        }


def deep_copy_mock_transcribe_call_fixture(
    mock_transcribe_call_fixture: MockTranscribeCallFixture,
) -> MockTranscribeCallFixture:
    return MockTranscribeCallFixture(**mock_transcribe_call_fixture.to_dict())


def mock_transcribe_call_fixture_from_yaml(yaml_path: str) -> MockTranscribeCallFixture:
    return MockTranscribeCallFixture(**yaml_load(yaml_path))


class MockTranscriptions:
    """
    Test-helper class for mocking the TranscriptionService
    (which is presumably an online API).

    To use, create a mock-transcribe-call.yaml file in the root
    of a test-mentor directory (see the examples under fixtures for the format)
    then call `mock_transcribe_result_and_callbacks`
    """

    def __init__(
        self, mock_init_transcription_service: Mock, source_file_root_path: str
    ):
        self.mock_service = Mock()
        self.source_file_root_path = source_file_root_path
        self.on_update_expected_calls: List[_Call] = []
        self.on_update_spy = Mock()
        mock_init_transcription_service.return_value = self.mock_service

    def _adjust_source_file_paths(self, result: TranscribeBatchResult) -> None:
        for j in result.transcribeJobsById.values():
            j.sourceFile = os.path.join(self.source_file_root_path, j.sourceFile)

    def expect_on_update_called_once_per_fixture_update(self) -> None:
        if self.on_update_expected_calls:
            self.on_update_spy.assert_has_calls(self.on_update_expected_calls)

    def mock_on_update(self) -> Callable[[TranscribeJobsUpdate], None]:
        def _on_update(update: TranscribeJobsUpdate) -> None:
            self.on_update_spy(update)

        return _on_update

    def mock_transcribe_result(self, mock_jobs: List[MockTranscribeJob]) -> None:
        result = TranscribeBatchResult()
        for j in mock_jobs:
            j.add_result(result)
        self.mock_transcribe_result_and_callbacks(
            MockTranscribeCallFixture(result=result)
        )

    def mock_transcribe_result_and_callbacks(
        self, mock_transcribe_call: MockTranscribeCallFixture
    ) -> None:
        mock_transcribe_call = deep_copy_mock_transcribe_call_fixture(
            mock_transcribe_call
        )
        self._adjust_source_file_paths(mock_transcribe_call.result)
        for j in mock_transcribe_call.result.transcribeJobsById.values():
            j.sourceFile = os.path.join(self.source_file_root_path, j.sourceFile)
        if mock_transcribe_call.updates:
            for u in mock_transcribe_call.updates:
                self._adjust_source_file_paths(u.result)
                self.on_update_expected_calls.append(call(u))

        def _transcribe(
            transcribe_requests: List[TranscribeJobRequest],
            batch_id: str = "",
            on_update: Optional[Callable[[TranscribeJobsUpdate], None]] = None,
            poll_interval=5,
        ) -> TranscribeBatchResult:
            if on_update:
                for u in mock_transcribe_call.updates:
                    on_update(u)
            return mock_transcribe_call.result

        self.mock_service.transcribe.side_effect = _transcribe
