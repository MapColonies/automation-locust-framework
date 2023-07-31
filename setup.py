import os

import setuptools

package_name = "automation_locust_framework"
author_name = "Dimitry"

# Check if requirements.txt and README.md exist
if not os.path.exists("requirements.txt"):
    raise FileNotFoundError("requirements.txt not found")

if not os.path.exists("README.md"):
    raise FileNotFoundError("README.md not found")

with open("requirements.txt", encoding="utf-8") as f:
    requirements = f.read().splitlines()

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name=package_name,
    version="0.1.0",  # Replace with the desired version number
    author=author_name,
    description="Map colonies performance infrastructure",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MapColonies/automation-locust-framework.git",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    zip_safe=False,  # Set to False if needed
)
