# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='judge_offline',
    version='0.1.0',
    description='Provides personal judge similar hackrank or judge online',
    long_description=readme,
    author='Yann Davin',
    author_email='yann.davin@gmail.com',
    url='https://github.com/yanndavin/judge_offline',
    license=license,
    packages=find_packages(exclude=('samples', 'docs'))
)