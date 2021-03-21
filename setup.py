# -*- coding: utf-8 -*-
""""""


from setuptools import setup


setup(
    name='buzfu',  # Required

    version='0.0.1',  # Required

    description='Tool that makes backgrounds useful ;)',  # Optional

    py_modules=["buzfu"],  # Required

    python_requires='>=3.6',

    install_requires=[
        "pandas",
        "requests",
        "cachetools",
        "matplotlib",
    ],  # Optional

    entry_points={  # Optional
        'console_scripts': [
            'buzfu=buzfu:main',
        ],
    },
)
