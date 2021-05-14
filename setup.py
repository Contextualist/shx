import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="shx",
    version="0.2.0",
    author="Contextualist",
    description="For writing async script with Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Contextualist/shx",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "aiocontextvars>=0.2.2; python_version < '3.7'",
    ],
    tests_require = [
        "pytest",
        "pytest-asyncio",
    ],
    entry_points = {
        "console_scripts": ["shx=shx.shx:main"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: AsyncIO",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: System :: Shells",
        "Topic :: Utilities",
    ],
)
