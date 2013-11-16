# [Automium Build Automation](http://automium.com)

Simple system for running build automation scripts.

## Usage

The basic usage of the automium utility assumes the location of the
build file under `build.json`

    atm
    
In order to be able to change the default build file the extra file
parameter must be provided.

    atm --file=extra.json

It's possible to verify changes from previous version, for that the
`--previous` parameter should be passed with the previous version.

    atm --previous=d86f4df6f7c9237a56970a102bba3482d91e823a

    atm --keep
    atm --keep --file=extra.json
    atm --pack
    atm --pack --file=extra.json

## Requirements

For linux based systems `dpkg-architecture` util is required to correctly retrieve the architecture for the system,
in case the utility does not exists an erroneous value may be present for build artifacts.

To install the command under Ubuntu Linux use the folowing command:

    apt-get install dpkg-dev
