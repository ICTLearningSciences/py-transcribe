from transcribe import TranscribeBatchResult, TranscribeJobRequest


def test_it_returns_jobs():
    batch_result = TranscribeBatchResult(
        transcribeJobsById=dict(
            job1=TranscribeJobRequest(sourceFile="x", jobId="job1").to_job(),
            job2=TranscribeJobRequest(sourceFile="y", jobId="job2").to_job(),
        )
    )
    assert list(batch_result.jobs())[0].get_fq_id() == "job1"
    assert list(batch_result.jobs())[1].get_fq_id() == "job2"


def test_it_first_job_as_a_convenience_for_single_job_requests():
    batch_result = TranscribeBatchResult(
        transcribeJobsById=dict(
            job1=TranscribeJobRequest(sourceFile="x", jobId="job1").to_job(),
            job2=TranscribeJobRequest(sourceFile="y", jobId="job2").to_job(),
        )
    )
    assert batch_result.first().get_fq_id() == "job1"
