from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='ESG Engine',
    version='0.1.5',
    description='A little online game engine.',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='Yannis300307',
    keywords=['python', 'Game Engine', "Pygame"],
    url='https://github.com/yannis300307/ES_Engine',
    download_url='',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)

install_requires = ["pygame"]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
