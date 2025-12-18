"""
Setup file for Pipeline Monitor Dashboard
"""
from setuptools import setup, find_packages
import os

# Read requirements from requirements.txt
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    with open(requirements_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='pipeline-monitor-dashboard',
    version='1.0.0',
    description='Pipeline monitor dashboard for Termius',
    author='Tahmid',
    python_requires='>=3.10',
    packages=find_packages(exclude=['tests', 'log', '__pycache__']),
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            # Add any command-line scripts here if needed
        ],     
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    include_package_data=True,
    zip_safe=False,
)

