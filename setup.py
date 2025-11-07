from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="callimachina",
    version="3.1.0",
    author="Hunter Shannon",
    author_email="hunter@shannonlabs.dev",
    description="The Alexandria Reconstruction Protocol - Autonomous Digital Archaeology",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Shannon-Labs/callimachina",
    packages=find_packages(where="callimachina/src"),
    package_dir={"": "callimachina"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
        ],
        "nlp": [
            "transformers>=4.30.0",
            "torch>=2.0.0",
        ],
        "db": [
            "sqlalchemy>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "callimachina=src.cli:callimachina",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)