cmake_minimum_required(VERSION 3.15...3.22)

project(${SKBUILD_PROJECT_NAME} VERSION ${SKBUILD_PROJECT_VERSION})

find_package(pybind11 CONFIG REQUIRED)

# emodlib src files
set(EMODLIB_OBJECTS
    ${CMAKE_SOURCE_DIR}/include/emodlib/malaria/InfectionMalaria.cpp
    ${CMAKE_SOURCE_DIR}/include/emodlib/malaria/SusceptibilityMalaria.cpp
    ${CMAKE_SOURCE_DIR}/include/emodlib/malaria/IntrahostComponent.cpp
    ${CMAKE_SOURCE_DIR}/include/emodlib/malaria/MalariaAntibody.cpp
    ${CMAKE_SOURCE_DIR}/include/emodlib/utils/RANDOM.cpp
    ${CMAKE_SOURCE_DIR}/include/emodlib/utils/suids.cpp)

pybind11_add_module(_emodlib_py src/main.cpp ${EMODLIB_OBJECTS})

# top-level directory for full include paths
target_include_directories(_emodlib_py PUBLIC ${CMAKE_SOURCE_DIR}/include)

target_compile_features(_emodlib_py PUBLIC cxx_std_14)
target_compile_definitions(_emodlib_py PRIVATE VERSION_INFO=${PROJECT_VERSION})

install(TARGETS _emodlib_py DESTINATION emodlib)
