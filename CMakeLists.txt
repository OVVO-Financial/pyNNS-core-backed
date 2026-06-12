cmake_minimum_required(VERSION 3.18)

project(pynns_native LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)
find_package(nanobind CONFIG REQUIRED)

set(NNSCORE_BUILD_TESTS OFF CACHE BOOL "Build NNS-core tests" FORCE)
set(NNSCORE_BUILD_PYTHON OFF CACHE BOOL "Build NNS-core Python bindings" FORCE)
add_subdirectory(extern/NNS-core)

nanobind_add_module(_nnscore src/pynns/_nnscore_bindings.cpp)
target_link_libraries(_nnscore PRIVATE nnscore)
target_compile_features(_nnscore PRIVATE cxx_std_17)
install(TARGETS _nnscore LIBRARY DESTINATION pynns)
