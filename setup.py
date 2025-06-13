from setuptools import setup, find_packages

setup(
    name="academic-research-automation-system",
    version="1.0.0",
    description="A comprehensive multi-agent system for automating academic research workflows",
    author="ARAS Team",
    author_email="contact@aras-project.org",
    url="https://github.com/yourusername/academic-research-automation-system",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "pandas>=1.2.0",
        "openpyxl>=3.0.5",
        "PyPDF2>=2.0.0",
        "pdfplumber>=0.5.0",
        "pytesseract>=0.3.0",
        "pdf2image>=1.14.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "black>=20.8b1",
            "flake8>=3.8.0",
            "sphinx>=3.0.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Text Processing :: Markup",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "aras=main:main",
        ],
    },
)
