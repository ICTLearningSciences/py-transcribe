py-transcribe
===================

Framework for synchronous batch text-to-speech transcription with backend services such as AWS, Watson, etc.

Python Installation
-------------------

```
pip install --user -e git+https://github.com/ictlearningsciences/py-transcribe.git@{release-tag}#egg=transcribe
```


Development
-----------

Run tests during development with

```
make test-all
```

Once ready to release, create a release tag, currently using semver-ish numbering, e.g. `1.0.0(-alpha.1)`