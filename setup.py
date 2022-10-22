from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("VERSION", "r", encoding="utf-8") as ver:
    version = ver.read()

setup(name='diefpy',
      version=version,
      packages=['diefpy'],
      license='MIT',
      author='Philipp D. Rohde, Nikoleta Themeliotou',
      author_email='philipp.rohde@tib.eu',
      url='https://github.com/SDM-TIB/diefpy',
      download_url='https://github.com/SDM-TIB/diefpy/archive/refs/tags/v' + version + '.tar.gz',
      project_urls={
            "Bug Tracker": "https://github.com/SDM-TIB/diefpy/issues",
      },
      description='Python package for computing diefficiency metrics dief@t and dief@k.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      keywords='metrics benchmarking efficiency diefficiency-metrics dief python',
      install_requires=['matplotlib>=3.2.2', 'numpy>=1.8.0'],
      include_package_data=True,
      package_data={'dief': ['data/*']},
      python_requires='>=3.6',
      classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Framework :: Matplotlib',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Topic :: System :: Benchmark',
            'Typing :: Typed'
      ])
