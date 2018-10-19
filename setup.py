import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rpi",
    version="0.0.1",
    author="Brian Tom",
    author_email="btom.0831@gmail.com",
    description="Control a Raspberry Pi over a network via REST.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BTx123/rpi-api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
