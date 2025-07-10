import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tideway",
    version="0.2.1",
    author="Wes Moskal-Fitzpatrick",
    author_email="wes@traversys.io",
    description="Library for BMC Discovery API Interface.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/traversys/Tideway",
    packages=setuptools.find_packages(exclude=["tests*"]),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
