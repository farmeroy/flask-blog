from setuptools import find_packages, setup

setup(
        name='flaskr',
        version='1.0.0',
        package=find_packages(),
        include_package_data=True,
        zip_safe=False,
        install_require=[
            'flask',
            ]
        )

