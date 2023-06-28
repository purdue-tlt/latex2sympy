#!/bin/sh

# variables
# get the current os and arch
os="$(uname -s)"
arch="$(uname -m)"
out_dir="$(realpath .)/src/latex2sympy/lib"
conan_setting_arch=$arch
generator="Unix Makefiles"
should_clean=true

setup()
{
	# Get relative path of the root directory of the project
	rdir=`git rev-parse --git-dir`
	rel_path="$(dirname "$rdir")"
	# Change to that path and run the file
	cd $rel_path

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
		echo "compiling on $os is not supported"
		exit 1
	fi

	echo ''
	# Activate virtual environment
	echo 'activate venv...'
	if test -f .env/bin/activate; then
		. .env/bin/activate && echo 'venv activated (bin)'
	elif test -f .env/Scripts/activate; then
		. .env/Scripts/activate && echo 'venv activated (Scripts)'
	else
		exit 1
	fi
}

clean()
{
	if [ $should_clean = true ]; then
		echo ''
		echo 'clean build files...'
		rm -rf build
		echo 'build files cleaned'
	fi
}

compile()
{
	clean

	if [ ! -d build ]; then
		mkdir build
	fi

	echo ''
	echo "generate and compile cpp parser (os: $os, arch: $arch, generator: $generator, conan_setting_arch: $conan_setting_arch, out_dir: $out_dir)..."
	cd build
	cmake .. -G "$generator" -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$out_dir" -DCONAN_SETTING_ARCH="$conan_setting_arch"
	make install
	echo 'cpp parser generated and compiled'

	clean
}

# get options
while getopts ':n' flag
do
	case $flag in
		n) # no clean
			echo 'using option "n": no clean'
			should_clean=false;;
		\?) # Invalid option
			echo 'Error: Invalid option'
			exit;;
	esac
done

setup
compile
exit 0
