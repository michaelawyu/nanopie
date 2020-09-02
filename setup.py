import re

from setuptools import find_packages, setup

with open("README.md", "rt") as f:
    readme = f.read()

with open("src/nanopie/__init__.py", "rt") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name="nanopie",
    version=version,
    url="https://github.com/michaelawyu/nanopie",
    project_urls={
        "Source": "https://github.com/michaelawyu/nanopie",
        "Documentation": "https://nanopie.readthedocs.io",
        "Issue Tracker": "https://github.com/michaelawyu/nanopie/issues",
    },
    license="Apache License 2.0",
    author="michaelawyu",
    author_email="michael.a.w.yu@gmail.com",
    maintainer="michaelawyu",
    maintainer_email="michael.a.w.yu@gmail.com",
    description="A lightweight framework for building Python microservices and API services.",
    long_description=readme,
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},
    python_requires=">3.4",
    install_requires=[],
    extras_require={
        "dev": [
            "pylint",
            "pytest",
            "black",
            "opentelemetry-api",
            "opentelemetry-sdk",
            "flask",
            "pyjwt",
            "cryptography",
            "twine",
        ],
        "docs": ["mkdocs", "mkdocs-material"],
    },
)
