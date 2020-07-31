import codecs
import os
import re

from setuptools import setup, find_packages, Command
from django_api_client.utils import get_version_from_changes

here = os.path.abspath(os.path.dirname(__file__))
version = get_version_from_changes(here)


# Save last Version
def save_version():
    version_path = os.path.join(here, "django_api_client/version.py")

    with open(version_path) as version_file_read:
        content_file = version_file_read.read()

    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(VSRE, content_file, re.M)
    current_version = mo.group(1)

    content_file = content_file.replace(current_version, "{}".format(version))

    with open(version_path, 'w') as version_file_write:
        version_file_write.write(content_file)


save_version()


# Get the long description
with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# Get changelog
with codecs.open(os.path.join(here, 'CHANGES.rst'), encoding='utf-8') as f:
    changelog = f.read()

with codecs.open(os.path.join(here, 'requirements.txt')) as f:
    install_requires = [line for line in f.readlines() if not line.startswith('#')]


class VersionCommand(Command):
    description = 'print library version'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print(version)


setup(
    author='Rafael Henter',
    author_email='rafael@henter.com.br',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries',
    ],
    cmdclass={'version': VersionCommand},
    description='Library with REST APIs Client code for Django',
    install_requires=install_requires,
    keywords='django rest views utils tools list api client restframework',
    long_description=long_description,
    name='django-api-client',
    packages=find_packages(exclude=['docs_src', 'doc', 'tests*']),
    url='https://github.com/rhenter/django-api-client',
    version=version,
)
