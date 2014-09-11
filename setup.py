from distutils.core import setup


setup(
	name="filmstrain",
	version='0.1.0',
	author='Sourav Chatterjee',
	author_email='souravc83@gmail.com',
	packages=['filmstrain'],
	package_dir={'filmstrain':'filmstrain'},
	description='FilmStrain: A python library to analyze arch and\
	             cantilever bending and calculate associated\
	             energy and strains from experimental data.',
	requires=["python(==2.7)",
               "matplotlib(>=1.1)",
                "numpy",
             ],
    provides=["filmstrain"]	
    )
