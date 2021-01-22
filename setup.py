import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tideway",
    version="0.1.0",
    author="Wes Moskal-Fitzpatrick",
    author_email="wes@traversys.io",
    description="library for BMC Discovery API Interface.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/traversys/tideway",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
    install_requires=[
        'requests',
    ]
)
