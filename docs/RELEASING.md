# Notes to Selves

- Start by updating `zversion.py`

- We only use major, minor, and point releases (x.y.z)

- To bump the release, modify `zversion.py`. At some point, we may add a "version bumping" framework, e.g. bump2version, but I don't see an immediate need for this yet.

- Commit the changes

- Tag a release in GitHub. Note that releasing on PyPI and releasing on GitHub are two different things. You can avoid having to keep track by runnign `git tag $(python setup.py --version)`. This will give the version that is associated with the Python setup.py file and use it not only to make a release but to ensure this release triggers a release on PyPI.

- Make sure not only to `git push` but to `git push --tags`.
