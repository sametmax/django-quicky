# -*- coding: utf-8 -*-



from setuptools import setup, find_packages

open('MANIFEST.in', 'w').write('\n'.join((
    "include *.md",
    "recursive-include django_quicky *.html",
)))

setup(

    name="django-quicky",
    version="0.7.1",
    packages=find_packages('.'),
    author="Sam et Max",
    author_email="lesametlemax@gmail.com",
    description="A collection of tools to make setting up Django quicker.",
    long_description=open('README.md').read(),
    include_package_data=True,
    install_requires=['django'],
    classifiers=[
        'Programming Language :: Python',
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: zlib/libpng License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3"
    ],
    url="https://github.com/sametmax/django-quicky"
)

