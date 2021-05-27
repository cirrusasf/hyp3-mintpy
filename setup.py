from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'hyp3-mintpy'
LONG_DESCRIPTION = 'hyp3-mintpy package is used to create time series analysis by mintpy package and with infm products produced with hyp3'

# Setting up
setup(
       # the name must match the folder name 'hyp3mintpy'
        name="hyp3mintpy", 
        version=VERSION,
        author="Jiang Zhu",
        author_email="<youremail@email.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'hyp3mintpy package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
        ]
)
