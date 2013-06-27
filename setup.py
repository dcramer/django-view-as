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
    version='0.2.4',
    description="A Django middleware which allows you to view the site on behalf of a user.",
    author="David Cramer",
    author_email="dcramer@gmail.com",
    license='Apache License 2.0',
    package_dir={'': 'src'},
    packages=find_packages("src"),
    include_package_data=True,
    install_requires=requires,
    extras_require={
        'tests': tests_require,
    },
    entry_points=entry_points,
    zip_safe=False,
)
