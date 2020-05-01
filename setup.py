from distutils.core import setup
from setuptools import find_packages
import ppjoin


with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

# with open('requirements.txt', 'r') as f:
#     install_requires = list()
#     dependency_links = list()
#     for line in f:
#         re = line.strip()
#         if re:
#             if re.startswith('git+') or re.startswith('svn+') or re.startswith('hg+'):
#                 dependency_links.append(re)
#             else:
#                 install_requires.append(re)

packages = find_packages()

setup(
    name='ppjoin',
    version=ppjoin.__version__,
    packages=packages,
    url='https://github.com/usc-isi-i2/ppjoin',
    project_urls={
        "Bug Tracker": "https://github.com/usc-isi-i2/ppjoin/issues",
        "Source Code": "https://github.com/usc-isi-i2/ppjoin",
    },
    license='MIT',
    author=ppjoin.__author__,
    author_email=ppjoin.__email__,
    description='PPJoin and P4Join Python 3 implementation',
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    # install_requires=install_requires,
    # dependency_links=dependency_links,
    classifiers=(
        "Programming Language :: Python :: 3",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology"
    )
)