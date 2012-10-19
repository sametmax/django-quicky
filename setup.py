
from setuptools import setup, find_packages

open('MANIFEST.in', 'w').write('\n'.join((
    "include *.md",
)))

setup(

    name="django-quicky",
    version="0.4.4",
    packages=find_packages('.'),
    author="Sam et Max",
    author_email="lesametlemax@gmail.com",
    description="A collection of toys to skip the forplay with Django and go straight to the point: url and view decorators",
    long_description=open('README.md').read(),
    include_package_data=True,
    install_requires=['django'],
    classifiers=[
        'Programming Language :: Python',
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: zlib/libpng License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7"
    ],
    url="https://github.com/sametmax/django-quicky"
)

