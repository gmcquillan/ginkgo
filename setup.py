#!/usr/bin/env python
import os
from setuptools import Command
from setuptools import setup, find_packages

def command(fn):
    def wrapped():
        class cmdclass(Command):
            def initialize_options(self): pass
            def finalize_options(self): pass
            user_options = []
            description = fn.__doc__
            def run(self): fn()
        return cmdclass
    return wrapped

@command    
def test():
    """run tests with nose"""
    os.execlp("nosetests", "nosetests")

@command
def build_pages():
    """rebuild the website"""
    os.execlp("bash", "bash", "-c", """branch=$(git status | grep 'On branch' | cut -f 4 -d ' ')
        git checkout gh-pages && 
        git commit --allow-empty -m 'trigger pages rebuild' && 
        git push origin gh-pages && 
        git checkout $branch""")

@command
def coverage():
    """run test coverage report with nose"""
    os.execlp("nosetests", "nosetests", "--with-coverage",
            "--cover-package=ginkgo")

setup(
    name='Ginkgo',
    version='0.5.0dev',
    author='Jeff Lindsay',
    author_email='jeff.lindsay@twilio.com',
    description='Lightweight service framework',
    packages=find_packages(),
    install_requires=['gevent==0.13.3', 'nose', 'python-daemon',],
    data_files=[],
    entry_points={
        'console_scripts': [
            'ginkgo = ginkgo.runner:main',]},
    cmdclass={
        'test': test(),
        'coverage': coverage(),
        'build_pages': build_pages(),}
)
