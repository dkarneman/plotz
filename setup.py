
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="plotz",
    version="0.0.1",
    author="Daniel Arneman",
    author_email=None,
    description="Graphing shortcuts with Pandas and Plotly",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dkarneman/plotz",
    packages=setuptools.find_packages(),
    install_requires=[
      'pandas',
      'plotly'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)