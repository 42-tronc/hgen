#!/bin/bash

# The script takes one argument, which determines the type of version update.
TYPE=$1

# Function to clean up the 'dist' directory
cleanup() {
	rm dist/* 2> /dev/null
}

# Function to update the version using semver.py script
setup_semver() {
	TYPE=$1
	python3 semver.py "$TYPE"
}

# Function to build the package
build() {
	python3 -m build
}

# Function to upload the package to the test PyPI repository
upload() {
	# python3 -m twine upload dist/*
	python3 -m twine upload --repository testpypi dist/*
}

# Function to refresh dependencies and push the changes to the git repository
refresh() {
	sleep 1
	pip3 install --upgrade genheader
	asdf reshim
}

# Function to commit and tag the release version, then push to the git repository
push() {
	git commit -am "release@$VER"
	git tag -a "$VER" -m "release@$VER"
	git push
}

# Clean up the 'dist' directory
cleanup

# Set the version using semver.py script
VER="v$(setup_semver "$TYPE")"

# Build the package
build

# Upload the package to the test PyPI repository
upload

# Refresh dependencies and push the changes
refresh

# Commit, tag, and push the release version
push
