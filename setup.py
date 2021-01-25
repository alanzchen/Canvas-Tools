import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="canvas-tools",
    version="0.0.1",
    author="Alan Chen",
    author_email="me@zenan.ch",
    description="A set of tools for working with Canvas.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alanzchen/Canvas-Tools",
    packages=setuptools.find_packages(),
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'canvas_group_csv=canvas_tools.canvas_group_csv:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)