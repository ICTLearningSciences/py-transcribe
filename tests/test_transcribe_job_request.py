from transcribe import TranscribeJobRequest


def test_it_generates_a_job_id_by_default():
    sourceFile = "/path/to/myfile3.mp3"
    job_req = TranscribeJobRequest(sourceFile=sourceFile)
    assert bool(job_req.jobId)
    assert job_req.jobId.startswith("myfile3-")
    assert len(job_req.jobId) > len("myfile3-") + 6


def test_it_preserves_job_id_when_set():
    sourceFile = "/path/to/myfile3.mp3"
    job_req = TranscribeJobRequest(sourceFile=sourceFile, jobId="myJobId1")
    assert job_req.jobId == "myJobId1"
