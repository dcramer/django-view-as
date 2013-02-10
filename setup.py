from setuptools import find_packages, setup

tests_require = [
    'mock',
    'pytest',
    'pytest-django',
]

requires = [
    'Django',
]

entry_points = {
}


setup(
    name='django-view-as',
    version='0.1.1',
    author="David Cramer",
    author_email="dcramer@gmail.com",
    license='Apache License 2.0',
    package_dir={'': 'src'},
    packages=find_packages("src"),
    install_requires=requires,
    extras_require={
        'tests': tests_require,
    },
    entry_points=entry_points,
    zip_safe=False,
)