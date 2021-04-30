from unittest.mock import patch, Mock

from transcribe import TranscribeJobRequest


@patch("transcribe.next_job_id")
def test_it_generates_a_job_id_by_default(mock_next_job_id: Mock):
    mock_next_job_id.return_value = "some-next-job-id"
    sourceFile = "/path/to/myfile3.mp3"
    job_req = TranscribeJobRequest(sourceFile=sourceFile)
    assert bool(job_req.jobId)
    assert job_req.jobId == "some-next-job-id"


def test_it_preserves_job_id_when_set():
    sourceFile = "/path/to/myfile3.mp3"
    job_req = TranscribeJobRequest(sourceFile=sourceFile, jobId="myJobId1")
    assert job_req.jobId == "myJobId1"
