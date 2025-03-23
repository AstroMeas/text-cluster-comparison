from setuptools import setup, find_packages
from pathlib import Path

cwd = Path(__file__).parent
req_path = cwd / 'requirements.txt'
# Fix encoding issue - try utf-8 first, then utf-16 if that fails
try:
    reqs = req_path.read_text(encoding='utf-8').split('\n')
except UnicodeDecodeError:
    reqs = req_path.read_text(encoding='utf-16').split('\n')

# Filter out empty requirements
reqs = [req for req in reqs if req.strip()]

# Read README.md for long description
long_description = (cwd / 'README.md').read_text(encoding='utf-8')

setup(
    name="text_cluster_compare",
    version="0.1.0",
    author='Rafael Deichsel',
    author_email='your.email@example.com',  # Add your email
    description="A tool for analyzing and visualizing textual similarities between two texts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/text-cluster-comparison",  # Add your GitHub repo URL
    packages=find_packages(),
    install_requires=reqs,
    include_package_data=True,
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Text Processing :: Linguistic",
        "Development Status :: 4 - Beta",
    ],
    keywords="text analysis, text comparison, clustering, linguistics, philology",
    project_urls={
        "Bug Tracker": "https://github.com/username/text-cluster-comparison/issues",
        "Documentation": "https://github.com/username/text-cluster-comparison",
        "Source Code": "https://github.com/username/text-cluster-comparison",
    },
    entry_points={
        "console_scripts": [
            "text-cluster-app=scripts.run_app:main",
        ],
    },
)