from setuptools import setup, find_packages

setup(
    name="your_project_name",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        # List your project's dependencies here, e.g.,
        # 'numpy>=1.18.0',
        # 'requests>=2.23.0',
    ],
    entry_points={
        'console_scripts': [
            # Define command-line scripts here, e.g.,
            # 'your_command=your_module:main_function',
        ],
    },
    author="jyolsna",
    author_email="isac.jyolsnaj@gmail.com",
    description="A chat application with Client-Server architecture using Python",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/your_project_name",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)