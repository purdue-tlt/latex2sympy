#!/bin/sh

# Get relative path of the root directory of the project
rdir=`git rev-parse --git-dir`
rel_path="$(dirname "$rdir")"
# Change to that path and run the file
cd $rel_path

# get the current os and arch
os="$(uname -s)"
arch="$(uname -m)"
out_dir="$(realpath ..)/src/latex2sympy"
conan_setting_arch=$os
generator="Unix Makefiles"

# update the output dir based on os and arch
if [ $os = "Darwin" ]; then
	if [ $arch = "arm64" ]; then
		out_dir="$out_dir/parser/macOS/arm64"
		conan_setting_arch="armv8"
	else
		out_dir="$out_dir/parser/macOS/x86_64"
	fi
elif [ $os = "Linux" ]; then
	out_dir="$out_dir/parser/linux"
else
	out_dir="$out_dir/parser/windows"
	generator="MSYS Makefiles"
fi

echo ''
echo "generate and compile cpp parser..."
rm -rf build
mkdir build
cd build
cmake .. -G "$generator" -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$out_dir" -DCONAN_SETTING_ARCH="$conan_setting_arch"
make install
echo "cpp parser generated and compiled"

exit 0