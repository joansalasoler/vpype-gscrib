from setuptools import setup


with open("README.md") as f:
    readme = f.read()

setup(
    name="vpype-gscrib",
    version="0.1.0",
    description="G-Code generator for Vpype",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Joan Sala",
    url="https://github.com/joansalasoler/vpype-gscrib",
    packages=["vpype_gscrib"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Topic :: Multimedia :: Graphics",
        "Environment :: Plugins",
    ],
    setup_requires=["wheel"],
    install_requires=[
        'click',
        'vpype[all]>=1.10,<2.0',
    ],
    entry_points='''
            [vpype.plugins]
            vpype_gscrib=vpype_gscrib.vpype_gscrib:vpype_gscrib
        ''',
)
