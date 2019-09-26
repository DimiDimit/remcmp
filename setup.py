from setuptools import setup


setup(
        name = "remcmp",
        version = "2.0",
        author = "DimiDimit",
        author_email = "dmtrdmtrov@gmail.com",
        description = "Extensible program to compare local and remote directories.",
        url = "https://github.com/DimiDimit/remcmp",
        packages = ["remcmp"],
        classifiers = [
            "Environment :: Console",
            "Natural Language :: English",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3"
        ],
        install_requires = ["colorama", "fs"],
        entry_points = {
            "console_scripts": [
                "remcmp = remcmp:main"
            ]
        }
)
