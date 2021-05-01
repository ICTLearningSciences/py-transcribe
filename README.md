# py-transcribe

Implementation-agnostic framework for synchronous batch text-to-speech transcription with backend services such as AWS, Watson, etc.

This module itself does NOT include a full implementation or an integration with any transcription service. The intention instead is that you include a specific implementation in your project. For example, for AWS Transcribe, use (py-transcribe-aws)[https://github.com/ICTLearningSciences/py-transcribe-aws]

## Python Installation

```
pip install py-transcribe
```

## Usage

You first need to install some concrete implementation of py-transcribe. If you are using AWS, then you can install `transcribe-aws` like this:

```bash
pip install py-transcribe-aws
```

...once the implementation is installed, you can configure that one of two ways:

### Setting the implementation module path

Set ENV var `TRANSCRIBE_MODULE_PATH`, e.g.

```bash
export TRANSCRIBE_MODULE_PATH=transcribe_aws
```

or pass the module path at service-creation time, e.g.

```python
from transcribe import init_transcription_service


service = init_transcription_service(
    module_path="transcribe_aws"
)
```

### Basic usage

Once you're set up, basic usage looks like this:

```python
from transcribe import (
    init_transcription_service
    TranscribeJobRequest,
    TranscribeJobStatus
)


service = init_transcription_service()
result = service.transcribe([
    TranscribeJobRequest(
        sourceFile="/some/path/j1.wav"
    ),
    TranscribeJobRequest(
        sourceFile="/some/other/path/j2.wav"
    )
])
for j in result.jobs():
    if j.status == TranscribeJoStatus.SUCCEEDED:
        print(j.transcript)
    else:
        print(j.error)
```

### Handling updates on large/long-running batch jobs

The main transcribe method is synchronous to hide the async/polling-based complexity of most transcribe services. But for any non-trivial batch of transcriptions, you probably do want to receive periodic updates, for example to save any completed transcriptions. You can do that by passing an `on_update` callback as follows:

```python
from transcribe import (
    init_transcription_service
    TranscribeJobRequest,
    TranscribeJobStatus,
    TranscribeJobsUpdate
)


service = init_transcription_service()


def _on_update(u: TranscribeJobsUpdate) -> None:
    for j in u.jobs():
        if j.status == TranscribeJoStatus.SUCCEEDED:
            print(f"save result: {j.transcript}")
        else:
            print(j.error)

result = service.transcribe(
    [
        TranscribeJobRequest(
            sourceFile="/some/path/j1.wav"
        ),
        TranscribeJobRequest(
            sourceFile="/some/other/path/j2.wav"
        )
    ],
    on_update=_on_update
)
```

### Configuring the environment for your implementation

Most implementations will also require other configuration, which you can either set in your environment or pass to `init_transcription_service` as `config={}`. See your implementation docs for details.


## Development

Run tests during development with

```
make test-all
```

Once ready to release, create a release tag, currently using semver-ish numbering, e.g. `1.0.0(-alpha.1)`
