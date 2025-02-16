"""
项目安装配置文件
"""
from setuptools import setup, find_packages

setup(
    name="share_content_matrix",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'python-dotenv',
        'plotly',
        'tushare'
    ],
) 