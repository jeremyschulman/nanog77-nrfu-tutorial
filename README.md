# Network Ready for Use - Test Automation

Network Ready for Use (NRFU) testing ansers the question:

_*Does the actual operating states of the network match the expected outcomes based on the design?*_

This repository contains NRFU for:

   * Execute tests using [PyTest](http://pytest.org)  
   * Get Arista EOS data via [eAPI](https://github.com/arista-eosplus/pyeapi)
   * Test functions:
        * check optic transceiver inventory
        * check interface status
        * check LLDP cabling for expected neighbor
        * check LAG interfaces
        * check MLAG control-plane status
        * check MLAG interface status
        * check BGP neighbor status
    
# Installation

Before you use this repository you will need to install a number of python packages.  I strongly suggest
you setup a virtual environment first.  Then you can run the following commands:

```bash
$ python setup.py develop
$ pip install -r requirements-develop.txt
```

# Quick Start - Offline Demo

If you'd like to see a demonstration the test-cases working immediately,
checkout the [offline-demo](offline-demo) directory.

```bash
cd offline-demo
./run-demo.sh dev1
```

This will run the tests for this repository, but you will see the output of the test-cases running
agaist fake data.  For more details, refer to the [offline-demo README.md](offline-demo/README.md).

# Online Demo

To execute the tests against a live Device Under Test (DUT) you can checkout the example pytest
testing files/functions defined in the [online-demo](online-demo) directory.  In order to perform
tests, there is also a script provided that will extract the existing information from your EOS device
to automatically create test-cases.  For more details, refer to the [online-demo README.md](online-demo/README.md).

