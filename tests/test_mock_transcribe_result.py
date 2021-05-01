from typing import List

import pytest
from unittest.mock import patch, Mock

import transcribe
from transcribe.mock import MockTranscribeJob, MockTranscriptions


@pytest.mark.parametrize(
    "mock_jobs,expected_result",
    [
        (
            [
                MockTranscribeJob(
                    batch_id="b1",
                    request=transcribe.TranscribeJobRequest(
                        jobId="j1", sourceFile="/fake/audio1.mp3"
                    ),
                    transcript="fake transcript result for audio 1!",
                )
            ],
            transcribe.TranscribeBatchResult(
                transcribeJobsById={
                    "b1-j1": transcribe.TranscribeJob(
                        batchId="b1",
                        jobId="j1",
                        mediaFormat="mp3",
                        sourceFile="/fake/audio1.mp3",
                        status=transcribe.TranscribeJobStatus.SUCCEEDED,
                        transcript="fake transcript result for audio 1!",
                    )
                }
            ),
        )
    ],
)
@patch.object(transcribe, "init_transcription_service")
def test_mocks_results_for_transcribe(
    mock_init_transcription_service: Mock,
    mock_jobs: List[MockTranscribeJob],
    expected_result: transcribe.TranscribeBatchResult,
):
    mock_transcriptions = MockTranscriptions(mock_init_transcription_service, ".")
    mock_transcriptions.mock_transcribe_result(mock_jobs)
    service = transcribe.init_transcription_service()
    result = service.transcribe([x.request for x in mock_jobs])
    assert result.to_dict() == expected_result.to_dict()
