from setuptools import setup

setup(
    name='showWeather',
    packages=['showweather'],
    include_package_data=True,
    install_requires=[
        'flask',
        'lxml',
        'requests',
        'cssselect'
    ],
)