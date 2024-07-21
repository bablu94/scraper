from setuptools import setup, find_packages

setup(
    name="scraper",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "requests",
        "beautifulsoup4",
        "pydantic",
        "cachetools",
    ],
    entry_points={
        "console_scripts": [
            "scraper=app.main:app",
        ],
    },
)
