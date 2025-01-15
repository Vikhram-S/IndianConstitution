from setuptools import setup, find_packages
import os

# Read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='iconlib',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # Add required packages here if necessary, e.g., 'requests', 'numpy'
    ],
    author='Vikhram S',
    author_email='vikhrams@saveetha.ac.in',
    description='A Python library for exploring the Constitution of India.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Vikhram-S/Iconlib',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: Civil Enthusiasts',
        'Topic :: Software Development :: Libraries',
    ],
    python_requires='>=3.7',
    extras_require={
        'dev': ['pytest', 'flake8'],
    },
    entry_points={
        'console_scripts': [
            'iconlib-cli=iconlib.__main__:main',
        ],
    },
    project_urls={
        'Documentation': 'https://github.com/Vikhram-S/Iconlib/blob/main/README.md',
        'Source Repository': 'https://github.com/Vikhram-S/Iconlib',
        'Issue Tracker': 'https://github.com/Vikhram-S/Iconlib/issues',
    },
)
