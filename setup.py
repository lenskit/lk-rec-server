import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="YOUR-USERNAME-HERE", # Replace with your own username
    version="0.0.1",
    author="Michael Ekstrand, Carlos Segura",
    author_email="michaelekstrand@boisestate.edu",
    description="The recommendation server for Lenskit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/carlos10seg/rec-service",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)