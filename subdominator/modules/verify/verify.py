import importlib.metadata as data
def getverify(pkg):
    version = data.version(pkg)
    return version