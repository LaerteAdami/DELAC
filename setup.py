import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

DEPENDENCIES = ['configargparse', "fenics-dolfin",
                "scipy", "cppimport", "numpy", "pyyaml"]

VERSION = "0.1"
URL = "https://github.com/LaerteAdami/DELAC"

setuptools.setup(
    name="turtleFSI",
    version=VERSION,
    license="GPL",
    author="Laerte Adami",
    author_email="laerte.adami@city.ac.uk",
    url=URL,
    project_urls={
        "Source Code": URL,
    },
    description="Deep Learning for Aerodynamic Control",
    long_description=long_description,
    long_description_content_type="text/markdown",

    # Dependencies
    install_requires=DEPENDENCIES,

    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        "Programming Language :: Python :: 3",
    ],
    packages=["DELAC",
              "DELAC.Aero",
              "DELAC.Mesh"],
    package_dir={"DELAC": "DELAC"}

)
