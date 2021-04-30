from transcribe import TranscribeJobRequest


def test_it_uses_batch_id_in_fully_qualified_name():
    sourceFile = "/path/to/anotherfile4.mp3"
    job_req = TranscribeJobRequest(sourceFile=sourceFile)
    job = job_req.to_job(batch_id="mybatch8")
    assert job.batchId == "mybatch8"
    assert job.get_fq_id().startswith("mybatch8-anotherfile4-")
