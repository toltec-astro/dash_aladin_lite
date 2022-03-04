import json
from setuptools import setup
from pathlib import Path

HERE = Path(__file__).parent

with open(HERE.joinpath('package.json')) as f:
    package = json.load(f)

package_name = package["name"].replace(" ", "_").replace("-", "_")

homepage = package['homepage']
repo_url = package['homepage']
bugs_url = package['bugs']['url']
long_description = (HERE / "README.md").read_text()


setup(
    name=package_name,
    version=package["version"],
    author=package['author'],
    packages=[package_name],
    include_package_data=True,
    license=package['license'],
    description=package.get('description', package_name),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=homepage,
    project_urls={
        "Bug Reports": bugs_url,
        "Source": repo_url,
    },
    install_requires=["dash"],
    classifiers=[
        "Framework :: Dash",
        'License :: OSI Approved :: BSD License',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
)
