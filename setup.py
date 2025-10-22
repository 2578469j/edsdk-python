import os
import sys
import platform
from setuptools import setup, Extension, find_packages

package_name = "edsdk-python"
version = "0.1"

here = os.path.abspath(os.path.dirname(__file__))

try:
    with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = ""


_DEBUG = True
_DEBUG_LEVEL = 0

# Detect platform
IS_WINDOWS = sys.platform == "win32"
IS_MACOS = sys.platform == "darwin"

EDSDK_PATH = "dependencies"
# EDSDK_PATH = "dependencies/EDSDK_13.13.41_Win/"

# Platform-specific configuration
if IS_WINDOWS:
    extra_compile_args = []
    if _DEBUG:
        extra_compile_args += ["/W4", "/DDEBUG=%s" % _DEBUG_LEVEL]
    else:
        extra_compile_args += ["/DNDEBUG"]

    extension = Extension(
        "edsdk.api",
        libraries=["EDSDK"],
        include_dirs=[os.path.join(EDSDK_PATH, "EDSDK/Header")],
        library_dirs=[os.path.join(EDSDK_PATH, "EDSDK_64/Library")],
        depends=["edsdk/edsdk_python.h", "edsdk/edsdk_utils.h"],
        sources=["edsdk/edsdk_python.cpp", "edsdk/edsdk_utils.cpp"],
        extra_compile_args=extra_compile_args,
    )

    data_files = [("Lib/site-packages/edsdk", [
        EDSDK_PATH + "/EDSDK_64/Dll/EDSDK.dll",
        EDSDK_PATH + "/EDSDK_64/Dll/EdsImage.dll"
    ])]

    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Environment :: Win32 (MS Windows)",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: System :: Hardware :: Universal Serial Bus (USB)",
        "Typing :: Stubs Only",
    ]

elif IS_MACOS:
    extra_compile_args = []
    extra_link_args = []

    if _DEBUG:
        extra_compile_args += ["-Wall", "-DDEBUG=%s" % _DEBUG_LEVEL]
    else:
        extra_compile_args += ["-DNDEBUG"]

    # Add C++11 support
    extra_compile_args += ["-std=c++11"]

    # macOS uses framework instead of static library
    framework_path = os.path.join(EDSDK_PATH, "EDSDK_Mac/Framework")

    extension = Extension(
        "edsdk.api",
        include_dirs=[os.path.join(EDSDK_PATH, "EDSDK/Header")],
        library_dirs=[framework_path],
        depends=["edsdk/edsdk_python.h", "edsdk/edsdk_utils.h"],
        sources=["edsdk/edsdk_python.cpp", "edsdk/edsdk_utils.cpp"],
        extra_compile_args=extra_compile_args,
        extra_link_args=[
            "-F" + framework_path,
            "-framework", "EDSDK",
            "-framework", "CoreFoundation",
            "-framework", "IOKit"
        ],
    )

    # On macOS, frameworks are typically handled differently
    # They should be bundled with the app or installed in system locations
    data_files = []

    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: System :: Hardware :: Universal Serial Bus (USB)",
        "Typing :: Stubs Only",
    ]

else:
    raise RuntimeError("Unsupported platform: %s" % sys.platform)

setup(
    name=package_name,
    version=version,
    author="Francesco Leacche",
    author_email="francescoleacche@gmail.com",
    url="https://github.com/jiloc/edsdk-python",
    description="Python wrapper for Canon EDSKD Library",
    long_description=long_description,
    ext_modules=[extension],
    install_requires=[
        'pywin32 >= 228 ; platform_system=="Windows"'
    ],
    setup_requires=["wheel"],
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "edsdk": ["py.typed", "api.pyi"],
    },
    data_files=data_files,
    python_requires=">=3.8.0",
    long_description_content_type="text/markdown",
    classifiers=classifiers,
    keywords=["edsdk", "canon"],
    license="MIT",
)
