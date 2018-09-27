# SPDX-License-Identifier: GPL-3.0+
from setuptools import setup, find_packages

requirements = []
with open('requirements.txt', 'r') as f:
    for requirement in f.readlines():
        if not requirement.startswith('-e'):
            requirements.append(requirement)

setup(
    name='review_rot_api',
    version='0.1',
    description='API used to query review-rot',
    author='Red Hat, Inc.',
    author_email='yashn@redhat.com',
    license='GPLv3+',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=requirements,
)
