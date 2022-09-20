from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="ezaws",
    version="0.25",
    package_dir={"ezaws": "src/ezaws"},
    packages=find_packages(exclude=("test*",)),
    description="An easy to use interface to AWS, ezaws.",
    url="https://github.com/saidvandeklundert/ezaws",
    classifiers=["Programming Language :: Python :: 3"],
    python_requires=">=3.10, <4",
    project_urls={
        "Bug Reports": "https://github.com/saidvandeklundert/ezaws/issues",
        "Source": "https://github.com/saidvandeklundert/ezaws",
        "Documentation": "https://github.com/saidvandeklundert/ezaws",
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
)
