from setuptools import setup, find_packages

setup(
    name = 'latr',
    version = '0.1.0',
    description = 'Lazy Iterator Chains',
    author = 'Brian Lauber',
    author_email = 'constructible.truth@gmail.com',
    packages = find_packages(exclude = ["tests"]),
    test_suite = 'tests',
    tests_require = ["mock>=1.0.0"]
)

