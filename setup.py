import setuptools

setuptools.setup(
    name="leonidas",
    version="1.0.0",
    author="bnwlkr",
    description="UBC Discord's Loyal Protector",
    url="https://github.com/bnwlkr/Leonidas",
    packages=setuptools.find_packages(),
    scripts=['runleonidas.py'],
    install_requires=[
        'discord',
        'python-dotenv',
        'aiohttp'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
