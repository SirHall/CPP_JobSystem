import fnmatch
import os

def RecursiveGlob(pathname, pattern):
    matches = []
    for root, dirnames, filenames in os.walk(pathname):
        for filename in fnmatch.filter(filenames, pattern):
            matchingFile = Glob(os.path.join(root, filename))
            relPath = os.path.join(root, filename)
            #matches.extend((matchingFile, relPath))
            matches.append(relPath)
    return matches

#Compile boost chrono library
chronoEnv = Environment( \
    CPPPath = [
        "dep/boost_chrono/include" \
        ], \
    CXXFLAGS = "-std=c++17")
chronoSrcs = RecursiveGlob("dep/boost_chrono/src/", "*.cpp");
chronoEnv.SharedLibrary("dep/boost_chrono/bin/boost_chrono", chronoSrcs)

#Compile boost system library
systemEnv = Environment( \
    CPPPath = [
        "dep/boost_system/include" \
        ], \
    CXXFLAGS = "-std=c++17")
systemSrcs = RecursiveGlob("dep/boost_system/src/", "*.cpp");
systemEnv.SharedLibrary("dep/boost_system/bin/boost_system", systemSrcs)

#Compile boost date_time library
date_timeEnv = Environment( \
    CPPPath = [
        "dep/boost_date_time/include" \
        ], \
    CXXFLAGS = "-std=c++17")
date_timeSrcs = RecursiveGlob("dep/boost_date_time/src/", "*.cpp");
date_timeEnv.SharedLibrary("dep/boost_date_time/bin/boost_date_time", \
    date_timeSrcs)


#Compile boost thread library
threadEnv = Environment( \
    CPPPath = [
        "dep/boost_thread/include", \
        "dep/boost_system/include", \
        "dep/boost_date_time/include", \
        "dep/boost_chrono/include", \
        "dep/boost_move/include"
    ], \
    CXXFLAGS = "-std=c++14 -lpthread " + \
        "-L./dep/boost_chrono/bin -L./dep/boost_system/bin -L./dep/boost_date_time" + \
        "-lboost_chrono -lboost_system -lboost_date_time", \
    LIBPATH = [ \
        "dep/boost_chrono/bin", \
        "dep/boost_system/bin", \
        "dep/boost_date_time/bin" \
    ], \
    LIBS = [ \
        "boost_chrono", \
        "boost_system", \
        "boost_date_time"
    ] \
)
threadSrcs = RecursiveGlob("dep/boost_thread/src/", "*.cpp");
threadEnv.SharedLibrary("dep/boost_thread/bin/boost_thread", threadSrcs)

#Compile program
progName = "out"
srcDir = "src"
includeDir = [
    "include"#, \
    # "dep/boost_bind/include", \
    # "dep/boost_thread/include", \
    # "dep/boost_asio/include"
]
libDirs = [ \
    # "#dep/boost_thread/bin/boost_thread.lib"
    # "boost_thread" \
]
buildDir = "build"
binDir = "bin"

#bt - build type. Use example: $ scons -bd=debug
cppFlags = {\
    "standard" : "-std=c++17 -pthread -lpthread -lboost_thread",\
    "debug" : "-std=c++17 -pthread -g",\
    "release" : "-std=c++17 -pthread -O3"\
}

usedCPPFlags = ""

if "bt" in ARGUMENTS:
    usedCPPFlags = cppFlags[ARGUMENTS["bt"]]
else:
    usedCPPFlags = cppFlags["standard"]

#print("\t\t" + usedCPPFlags)

env = Environment(CPPPATH = includeDir, CXXFLAGS = usedCPPFlags, \
    LIBPATH = libDirs)

env.VariantDir(variant_dir = buildDir, src_dir = srcDir, duplicate = 0)

srcs = RecursiveGlob(srcDir, "*.cpp")

#print([buildDir + "/" + f[4:] + "\n" for f in srcs])

var_srcs = [buildDir + "/" + f[4:] for f in srcs]

# env.Program(binDir + "/"  + progName, var_srcs)
