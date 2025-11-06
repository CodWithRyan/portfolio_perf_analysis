from setuptools import setup, find_packages
setup(
name="portfolio_perf_analysis",
version="0.1.0",
package_dir={"": "src"},
packages=find_packages(where="src"),
install_requires=[
"yfinance>=0.2.32",
"pandas>=2.0.0",
"numpy>=1.24.0",
"matplotlib>=3.7.0",
"seaborn>=0.12.0",
"tabulate>=0.9.0",
],
)
