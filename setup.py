import setuptools

setuptools.setup(
    name="tideway",
    version="0.3.0",
    author="Wes Moskal-Fitzpatrick",
    author_email="wes@traversys.io",
    description="Library for BMC Discovery API Interface.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/traversys/Tideway",
    packages=setuptools.find_packages(exclude=["tests*"]),
    install_requires=[
        "requests",
        "tabulate",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
