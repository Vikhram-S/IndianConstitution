from setuptools import setup, find_packages

setup(
    name='IndianConstitution',
    version='0.5.2',
    description='A Python module for accessing and managing Constitution data.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Vikhram S',
    author_email='vikhrams@saveetha.ac.in',
    url='https://github.com/Vikhram-S/Iconlib',
    license='Apache License 2.0',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    project_urls={
        'Documentation': 'https://github.com/Vikhram-S/Iconlib/blob/main/README.md',
        'Source': 'https://github.com/Vikhram-S/Iconlib',
        'Issue Tracker': 'https://github.com/Vikhram-S/Iconlib/issues',
    },
    zip_safe=False,  # Ensures compatibility with some environments
)
