from setuptools import setup, find_packages
from os import path


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


def _read_dependencies():
    requirements_file = "requirements.txt"
    with open(requirements_file) as fin:
        return [line.strip() for line in fin if line]


packages = find_packages()
requirements = _read_dependencies()

setup(
    name="posedetect_core",
    version="1.0.0",
    author_email="larrykirschner@gmail.com",
    description="python core types for posedetect",
    packages=packages,
    package_dir={'posedetect_core': 'posedetect_core'},
    package_data={'posedetect_core': ['data/fixtures/resources/videos/**/*']},
    install_requires=requirements,
    long_description=long_description,
    long_description_content_type='text/markdown',
)
