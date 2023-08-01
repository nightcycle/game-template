#!/usr/bin/env bash

# generate scripts
scripts/build/generation/midas.sh
scripts/build/generation/datatree.sh
scripts/build/generation/pseudo-enum.sh
scripts/build/generation/boot.sh
scripts/build/generation/style-guide.sh

# update wally
scripts/build/wally.sh

# update assets
scripts/build/asphalt.sh

# build scene
scripts/build/scene.sh

# generate final sourcemap
scripts/rojo/sourcemap.sh
