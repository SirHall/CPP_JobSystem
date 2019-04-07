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
    CPPPATH = [
        "dep/boost_chrono/include" \
        ], \
    CXXFLAGS = "-std=c++17")
chronoSrcs = RecursiveGlob("dep/boost_chrono/src/", "*.cpp");
chronoEnv.StaticLibrary("dep/boost_chrono/bin/boost_chrono", chronoSrcs)

#Compile boost system library
systemEnv = Environment( \
    CPPPATH = [
        "dep/boost_system/include" \
        ], \
    CXXFLAGS = "-std=c++17 -lpthread")
systemSrcs = RecursiveGlob("dep/boost_system/src/", "*.cpp");
systemEnv.StaticLibrary("dep/boost_system/bin/boost_system", systemSrcs)

#Compile boost date_time library
date_timeEnv = Environment( \
    CPPPATH = [
        "dep/boost_date_time/include" \
        ], \
    CXXFLAGS = "-std=c++17")
date_timeSrcs = RecursiveGlob("dep/boost_date_time/src/", "*.cpp");
date_timeEnv.StaticLibrary("dep/boost_date_time/bin/boost_date_time", \
    date_timeSrcs)


#Compile boost thread library
threadEnv = Environment( \
    CPPPATH = [
        "dep/boost_thread/include", \
        # "dep/boost_system/include", \
        # "dep/boost_date_time/include", \
        # "dep/boost_chrono/include", \
        "dep/boost_move/include", \
        "dep/boost_atomic/include", \
        "dep/boost_win_api/include"
    ], \
    CXXFLAGS = "-std=c++14 -lpthread " + \
        "-L./dep/boost_chrono/bin -L./dep/boost_system/bin " +\
        "-L./dep/boost_date_time -L./dep/boost_thread/src " + \
        "-lboost_chrono -lboost_system -lboost_date_time -lfuture -ltss_null", \
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
#We want to skip the win32 dir
threadSrcs = RecursiveGlob("dep/boost_thread/src/pthread", "*.cpp")
threadEnv.StaticLibrary("dep/boost_thread/bin/boost_thread", threadSrcs)

#Compile program
progName = "bin/out"
srcDir = "src"
includeDir = [
    "include"#, \
    # "dep/boost_bind/include", \
    # "dep/boost_thread/include", \
    # "dep/boost_asio/include"
]
libDirs = [ \
    "#dep/boost_thread/bin/", \
    "#dep/boost_system/bin/"
    # "boost_thread" \
]
libs =[ \
    "boost_thread", "boost_system", "pthread"
]
buildDir = "build"
binDir = "bin"

#bt - build type. Use example: $ scons -bd=debug
cppFlags = {\
    "standard" : "-std=c++17 -pthread -lpthread -L./dep/boost_thread/bin -lboost_thread",\
    "debug" : "-std=c++17 -lpthread -g",\
    "release" : "-std=c++17 -lpthread -O3"\
}

usedCPPFlags = ""

if "bt" in ARGUMENTS:
    usedCPPFlags = cppFlags[ARGUMENTS["bt"]]
else:
    usedCPPFlags = cppFlags["standard"]

#print("\t\t" + usedCPPFlags)

env = Environment(CPPPATH = includeDir, CXXFLAGS = usedCPPFlags, \
    LIBPATH = libDirs, LIBS = libs)

env.VariantDir(variant_dir = buildDir, src_dir = srcDir, duplicate = 0)

srcs = RecursiveGlob(srcDir, "*.cpp")

#print([buildDir + "/" + f[4:] + "\n" for f in srcs])

var_srcs = [buildDir + "/" + f[4:] for f in srcs]

env.Program(binDir + "/"  + progName, var_srcs)
