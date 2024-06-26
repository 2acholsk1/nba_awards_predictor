#!/usr/bin/env python3
"""
The MIT License (MIT)

Copyright (C) 2024 2acholsk1 - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license.
You should have received a copy of the MIT license with
this file.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal in the
Software without restriction, including without limitation the rights to use, copy,
modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""

import setuptools
from setuptools import setup


setup(
    name="NBA-Awards-Predictor",
    version="v1.0.1",
    author="2acholsk1",
    license="MIT",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'NBA_predict = src.__main__:main',
            'data_prepare = src.data_work.preparing:main',
            'data_team_prepare = src.data_work.preparing_teams:main',
            'data_format = src.data_work.formating:main',
            'data_link = src.data_work.linking:main',
            'model_test = src.model_work.testing:main',
            'model_train = src.model_work.train:main',
            'model_train_rookie = src.model_rookie_work.train:main',
            'model_feature_important = src.model_work.features_important:main',
            'model_feature_important_rookie = src.model_rookie_work.features_important:main',
            'model_params_search = src.model_work.parameters_search:main',
            'model_params_search_rookie = src.model_rookie_work.parameters_search:main',
        ],
    },
    python_requires='>=3.11',
)
