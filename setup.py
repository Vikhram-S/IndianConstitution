from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="IndianConstitution",
    version="1.0.1",
    description=(
        "AI- and NLP-enabled Python framework for programmatic access, "
        "analysis, and research on the Constitution of India."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Vikhram S",
    author_email="vikhrams@saveetha.ac.in",
    maintainer="Vikhram S",
    maintainer_email="vikhrams@saveetha.ac.in",

    url="https://github.com/Vikhram-S/IndianConstitution",

    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,

    python_requires=">=3.7",

    install_requires=[],

    extras_require={
        "analysis": [
            "pandas>=1.3.0",
            "matplotlib>=3.3.0",
        ],
        "search": [
            "fuzzywuzzy>=0.18.0",
            "python-Levenshtein>=0.12.0",
        ],
        "all": [
            "pandas>=1.3.0",
            "matplotlib>=3.3.0",
            "fuzzywuzzy>=0.18.0",
            "python-Levenshtein>=0.12.0",
        ],
    },

    entry_points={
        "console_scripts": [
            "indianconstitution=indianconstitution.cli:main",
        ],
    },

    license="Apache License 2.0",

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Legal Industry",
        "Intended Audience :: Science/Research",

        "License :: OSI Approved :: Apache Software License",

        "Natural Language :: English",
        "Operating System :: OS Independent",

        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",

        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Sociology",
        "Topic :: Education",
    ],

    keywords=[
        "constitution of india",
        "legaltech",
        "civic tech",
        "india ai",
        "nlp",
        "ai",
        "law",
        "policy research",
        "open data",
        "constitutional law",
    ],

    project_urls={
        "Documentation": "https://pypi.org/project/IndianConstitution/",
        "Source": "https://github.com/Vikhram-S/IndianConstitution",
        "Issue Tracker": "https://github.com/Vikhram-S/IndianConstitution/issues",
        "Changelog": "https://github.com/Vikhram-S/IndianConstitution/blob/main/changelog.md",
    },
)
