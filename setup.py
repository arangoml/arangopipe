import pathlib

from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).resolve().parents[0]

# The text of the README file
README = (HERE / "README.md").read_text()

requirements = [
    "python-arango",
    "pandas",
    "PyYAML==5.1.1",
    "sklearn2",
    "yapf",
    "autopep8",
    "requests"
]

# This call to setup() does all the work
setup(
    name="arangopipe",
    version="0.0.70.0.2",
    description="package for machine learning meta-data management and analysis",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/arangoml/arangopipe",
    author="ArangoDB",
    author_email="joerg@arangodb.com",
    license="Apache",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=[
        "arangopipe",
        "arangopipe.api",
        "arangopipe.analytics",
    ],
    package_data={"config": ["arangopipe/arangopipe_storage/arangopipe_config.yaml"]},
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.7",
    extras_require={
        "dev": [
            "black~=22.8",
            "flake8~=5.0",
            "isort~=5.10",
            "mypy~=0.982",
            "types-PyYAML~=6.0",
            "types-requests~=2.28",
            "types-urllib3~=1.26",
            "dynaconf==3.1.11",
        ]
    },
)
