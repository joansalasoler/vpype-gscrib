from setuptools import setup


with open("README.md") as f:
    readme = f.read()

setup(
    name="vpype-mecode",
    version="0.1.0",
    description="G-Code generator for Vpype",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Joan Sala",
    url="https://github.com/joansalasoler/vpype-mecode",
    packages=["vpype_mecode"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
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
            vpype_mecode=vpype_mecode.vpype_mecode:vpype_mecode
        ''',
)
