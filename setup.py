# encoding=utf8
import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

README = read('README.md')

setup(
    name = "django-media-tree",
    version = "0.1.0",
    url = 'http://github.com/philomat/django-media-tree',
    license = 'BSD',
    description = "Django Media Tree is a Django app for managing your website's media files in a folder tree, and using them in your own applications.",
    long_description = README,

    author = u'Samuel Luescher',
    author_email = 'philomat@popkultur.net',
    
    packages = find_packages(),
    include_package_data=True,

    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)

print find_packages()