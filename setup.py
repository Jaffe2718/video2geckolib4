from setuptools import setup, find_packages
import os

setup(
    name='video2geckolib4',
    version='0.1.0',
    author='Jaffe2718',  # 替换为你的名字
    author_email='qqyttwqeei@163.com',  # 替换为你的邮箱
    description='A package for converting video poses to GeckoLib4 animations',
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    url='https://github.com/Jaffe2718/video2geckolib4',  # 替换为你的项目仓库地址
    packages=find_packages(include=['video2geckolib4']),
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