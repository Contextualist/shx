import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="shx",
    version="0.4.2",
    author="Contextualist",
    description="For writing async script with Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Contextualist/shx",
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    install_requires=[],
    tests_require = [
        "pytest",
        "pytest-asyncio >= 0.17",
    ],
    entry_points = {
        "console_scripts": ["shx=shx.shx:main"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: AsyncIO",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: System :: Shells",
        "Topic :: Utilities",
    ],
)
