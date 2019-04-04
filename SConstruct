import fnmatch
import os

progName = "out"
srcDir = "src"
includeDir = ["include"]
buildDir = "build"
binDir = "bin"
cppFlags = "-O3"

def RecursiveGlob(pathname, pattern):
    matches = []
    for root, dirnames, filenames in os.walk(pathname):
        for filename in fnmatch.filter(filenames, pattern):
            matchingFile = Glob(os.path.join(root, filename))
            relPath = os.path.join(root, filename)
            #matches.extend((matchingFile, relPath))
            matches.append(relPath)
    return matches

env = Environment(CPPPATH = includeDir, CXXFLAGS = cppFlags)

env.VariantDir(variant_dir = buildDir, src_dir = srcDir, duplicate = 0)

srcs = RecursiveGlob(srcDir, "*.cpp")

#print([buildDir + "/" + f[4:] + "\n" for f in srcs])

var_srcs = [buildDir + "/" + f[4:] for f in srcs]

env.Program(binDir + "/"  + progName, var_srcs)
