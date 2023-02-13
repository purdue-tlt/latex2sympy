#!/bin/sh

# Get relative path of the root directory of the project
rdir=`git rev-parse --git-dir`
rel_path="$(dirname "$rdir")"
# Change to that path and run the file
cd $rel_path

# get the current os and arch
os="$(uname -s)"
arch="$(uname -m)"
out_dir="$(realpath .)/src/latex2sympy/lib"
conan_setting_arch=$arch
generator="Unix Makefiles"

# update the output dir based on os and arch
if [ $os = "Darwin" ]; then
	# update out_dir and conan arch, if need
	if [ $arch = "arm64" ]; then
		out_dir="$out_dir/macOS/arm64"
		conan_setting_arch="armv8"
	else
		out_dir="$out_dir/macOS/x86_64"
	fi
elif [ $os = "Linux" ]; then
	out_dir="$out_dir/linux"
else
	echo 'Compiling on $os not supported'
	exit 1
fi

echo ''
# Activate virtual environment
echo "activating venv..."
if test -f .env/bin/activate
then . .env/bin/activate && echo "venv activate (bin)"
elif test -f .env/Scripts/activate
then . .env/Scripts/activate && echo "venv activated (Scripts)"
else exit 1
fi

echo ''
echo "generate and compile cpp parser (os: $os, arch: $arch, generator: $generator, conan_setting_arch: $conan_setting_arch, out_dir: $out_dir)..."
rm -rf build
mkdir build
cd build
cmake .. -G "$generator" -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$out_dir" -DCONAN_SETTING_ARCH="$conan_setting_arch"
make install
echo "cpp parser generated and compiled"

rm -rf build
echo "build files cleaned"

exit 0