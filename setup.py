import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nif-api",
    version="0.3.21",
    author="Einar Huseby",
    author_email="einar.huseby@gmail.com",
    description="A pythonic interface to NIF webservices using Zeep",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/luftsport/nif-api",
    packages=setuptools.find_packages(),
    install_requires=['zeep', 'python-dateutil', 'inflection'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
