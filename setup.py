from setuptools import setup, find_packages

version = 'Flask REST service demo'

setup(name='epgdemo',
      version=version,
      description="",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Sergey Krushinsky',
      author_email='krushinsky@gmail.com',
      url='',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
            'flask >= 2.0.1',
            'schema >= 0.7.4',
            'python-json-logger >= 2.0.1'          
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
