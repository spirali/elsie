from setuptools import setup

setup(
    name="mkdocs-elsie-plugin",
    version="0.0.1",
    description="MkDocs plugin for building Elsie examples in documentation",
    author="Stanislav Böhm",
    author_email="spirali@kreatrix.org",
    url="https://github.com/spirali/elsie",
    packages=["mkdocs_elsie_plugin"],
    entry_points={
        'mkdocs.plugins': [
            'elsie = mkdocs_elsie_plugin:ElsiePlugin',
        ]
    }
)
