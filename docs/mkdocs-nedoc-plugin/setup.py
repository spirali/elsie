from setuptools import setup

setup(
    name="mkdocs-nedoc-plugin",
    version="0.0.1",
    description="Nedoc plugin for linking to API documentation",
    author="Stanislav Böhm",
    author_email="spirali@kreatrix.org",
    url="https://github.com/spirali/elsie",
    packages=["mkdocs_nedoc_plugin"],
    entry_points={
        'mkdocs.plugins': [
            'nedoc = mkdocs_nedoc_plugin:NedocPlugin',
        ]
    }
)
