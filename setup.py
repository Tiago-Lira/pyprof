from setuptools import find_packages, setup


setup(
    name='pyprof',
    author='Tiago Lira',
    author_email='tiagoliradsantos@gmail.com',
    version='0.0.1',
    packages=find_packages(),
    license='MIT',
    long_description=open('README.md').read(),
    install_requires=[
        'line-profiler==2.1.2',
    ],
    entry_points={
        "console_scripts": [
            "pyprof = pyprof.bin.prof:cli",
        ],
    },
)
