from setuptools import setup


install_requires = [
    "progressbar>=2.5",
]
test_require = []

dev_require = []

setup(
    name="mc_server_python",
    version="0.2",
    description="A Minecraft server setup script made using python3",
    author="Yot360",
    author_email="65982248+yot360@users.noreply.github.com",
    install_requires=install_requires,
    tests_require=test_require,
    extras_require={
        "tests": test_require,
        "dev": dev_require,
        "all": test_require + dev_require,
    },
    package_dir={"": "src"},
    packages=["mc_server_python"],
    entry_points={
        "console_scripts": [
            "mc_server_python=mc_server_python.__main__:cli"
        ],
    },
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.6"
)
