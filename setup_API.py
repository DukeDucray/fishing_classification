from setuptools import find_packages
from setuptools import setup

with open("requirements_image.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(name='fishing_classification',
      version="0.0.1",
      description="First Try",
      license="MIT",
      author="Team Fishing",
      author_email="pgducray@gmail.com",
      #url="https://github.com/lewagon/taxi-fare",
      install_requires=requirements,
      packages=find_packages(),
      test_suite="tests",
      # include_package_data: to install data from MANIFEST.in
      include_package_data=True,
      zip_safe=False)
