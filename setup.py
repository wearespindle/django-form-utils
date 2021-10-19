from setuptools import setup


long_description = open('README.rst').read() + '\n\n' + open('CHANGES.rst').read()

setup(
    name='django-form-utils',
    version='1.0.3.post',
    description='Form utilities for Django',
    long_description=long_description,
    author='Carl Meyer',
    author_email='carl@oddbird.net',
    url='http://bitbucket.org/carljm/django-form-utils/',
    packages=['form_utils', 'form_utils.templatetags'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Framework :: Django',
    ],
    zip_safe=False,
    package_data={'form_utils': ['templates/form_utils/*.html',
                                 'media/form_utils/js/*.js']},
    test_suite='tests.runtests.runtests',
    tests_require=['Django', 'mock', 'Pillow'],
)
