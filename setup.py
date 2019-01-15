import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="empyro",
    version="0.0.1",
    author="Ayman Izzeldin",
    description="Terminal emulator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aymanizz/empyro",
    packages=setuptools.find_packages(),
    python_requires='>=3.4',
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Terminals",
    ],
)
