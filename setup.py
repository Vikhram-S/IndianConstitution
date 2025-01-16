from setuptools import setup, find_packages
import os

# Read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='iconlib',
    version='0.3',
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
        'Development Status :: 4 - Beta',  
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries',
        'Topic :: Education',
        'Topic :: Utilities',
    ],
    keywords='constitution india python library educational',
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
        'Source': 'https://github.com/Vikhram-S/Iconlib',
        'Issue Tracker': 'https://github.com/Vikhram-S/Iconlib/issues',
    },
    license='Apache License 2.0',  # Explicit license field
    zip_safe=False,  # Ensures compatibility with some environments
)
