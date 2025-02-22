from setuptools import setup, find_packages
import os

setup(
    name='video2geckolib4',
    version='0.1.0',
    author='Jaffe2718',
    author_email='qqyttwqeei@163.com',
    description='A package for converting video poses to GeckoLib4 animations',
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    url='https://github.com/Jaffe2718/video2geckolib4',
    packages=find_packages(include=['video2geckolib4']),
    package_data={
        'video2geckolib4': ['basemodel.bbmodel']
    },
    install_requires=[
        'opencv-contrib-python',
        'mediapipe',
        'numpy',
        'scipy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)