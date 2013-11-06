# [Automium Build Automation](http://automium.com)

Simple system for running build automation scripts.

## Usage

    atm
    atm --keep
    atm --file=extra.json
    atm --keep --file=extra.json
    atm --pack
    atm --pack --file=extra.json

## Requirements

For linux based systems `dpkg-architecture` util is required to correctly retrieve the architecture for the system,
in case the utility does not exists an erroneous value may be present for build artifacts.

To install the command under Ubuntu Linux use the folowing command:

    apt-get install dpkg-dev
