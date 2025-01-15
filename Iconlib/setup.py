from setuptools import setup, find_packages
import urllib.request

# Reading the README file from GitHub URL
url = "https://raw.githubusercontent.com/Vikhram-S/Iconlib/main/README.md"
try:
    with urllib.request.urlopen(url) as response:
        long_description = response.read().decode('utf-8')
except Exception as e:
    long_description = "A Python library for exploring the Constitution of India."

setup(
    name="iconlib",
    version="1.0.0",
    author="Vikhram S",
    author_email="vikhrams@saveetha.ac.in",
    description="A Python library for exploring the Constitution of India.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/Vikhram-S/Iconlib",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Civil Enthusiasts",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.7",
    extras_require={
        "dev": ["pytest", "flake8"],
    },
    entry_points={
        "console_scripts": [
            "iconlib-cli=iconlib.__main__:main",
        ],
    },
    project_urls={
        "Documentation": "https://github.com/Vikhram-S/Iconlib/blob/main/README.md",
        "Source": "https://github.com/Vikhram-S/Iconlib",
        "Tracker": "https://github.com/Vikhram-S/Iconlib/issues",
    },
)
