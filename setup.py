from setuptools import setup, find_packages

setup(
    name='repoze-plugins',
    version='0.1',
    description='Plugins for repoze.who',
    url='http://github.com/drmalex07/repoze-plugins',
    author='Michail Alexakis',
    author_email='drmalex07@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['repoze.who.plugins'],
    install_requires=[
        # Note: Moved under requirements.txt
    ],
    setup_requires=[
    ],
    entry_points = {
    },
    zip_safe=False)

