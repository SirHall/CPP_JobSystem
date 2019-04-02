import fnmatch
import os

progName = "out"

def RecursiveGlob(pathname, pattern):
    matches = []
    for root, dirnames, filenames in os.walk(pathname):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(File(os.path.join(root, filename)))
    return matches

#VariantDir('build', 'include')

srcs = RecursiveGlob("src", "*.cpp")

#var_scrs = ["#bin/" + f for f in srcs]

env = Environment(CPPPATH = "include")

for f in srcs:
        fName = os.path.splitext(f.name)
        env.Object("build/" + fName[0] + ".o", f);

objs = Glob("build/*.o")

env.Program(progName, objs)
