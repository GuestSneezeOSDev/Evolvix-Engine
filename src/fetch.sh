#!/bin/bash
echo "Evolvix Fetch is fetching files"
git clone https://github.com/Vortex-Engine/vortex-engine
cd vortex-engine/sp/game/mod-hl2
echo "Installing files"
~/
cp -r materials ~/evolvix/sp # if it is sp then keep if it is mp then user has to do it themselves
cp -r models ~/evolvix/sp
cd ../../../..
rm -rf vortex-engine
echo "complete"

