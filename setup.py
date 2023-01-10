import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


setup(
    name='wiker',
    version='0.0.1',
    packages=find_packages(exclude=('tests', 'tests.*', 'examples.*', 'docs',)),
    url='https://github.com/anorprogrammer/wiker',
    license='MIT',
    author='Shahobiddin Anorboyev',
    python_requires='>=3.7',
    author_email='anorprogrammer1127@gmail.com',
    description='Library for wikipedia dataset collection',
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries',
    ],
    install_requires=[
        'beautifulsoup4>=4.11',
        'requests>=2.25'
    ],
    include_package_data=False,
)
