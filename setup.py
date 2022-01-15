from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()

        
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(name='diefpy',
      version='1.0.2',
      packages=['diefpy'],
      license='MIT',
      author='Philipp D. Rohde, Nikoleta Themeliotou',
      author_email='philipp.rohde@tib.eu',
      url='https://github.com/SDM-TIB/diefpy',
      download_url='https://github.com/SDM-TIB/diefpy/archive/refs/tags/v1.0.2.tar.gz',
      description='Python package for computing diefficiency metrics dief@t and dief@k.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      keywords='metrics benchmarking efficiency diefficiency-metrics dief python',
      install_requires=['matplotlib==3.2.2', 'numpy>=1.8.0'],
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
            'License :: OSI Approved :: MIT License',
            'Topic :: System :: Benchmark',
            'Typing :: Typed'
      ])
