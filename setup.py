from setuptools import setup, find_packages
from pathlib import Path

cwd = Path(__file__).parent
req_path = cwd / 'requirements.txt'
reqs = req_path.read_text(encoding='utf-16').split('\n')
print(reqs)
setup(
    name="text_cluster_compare",
    version="0.1.0",
    packages=find_packages(),
    install_requires=reqs,
    include_package_data=True,
    python_requires=">=3.7"
)
