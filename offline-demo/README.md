# Demo NRFU 

This directory contains a demonstration of using the NRFU EOS pytest functions by
dynamically loading test-cases based on pytest command line arguments:

    --nrfu-device : the name of the device
    --nrfu-testcasedir : the path to the device testcase files
    
This demonstrations uses EOS show output that was captured and stored into JSON
files rather than going directly to the EOS device; this was done for the purpose of
demonstrations and dev-testing so that there is no dependencies on actual running systems.

For an example of using NRFU EOS pytest with an actual device, refer to the
[online-demo](../online-demo) directory.

# Run

To run the demonstration:

```shell script
$ ./run-demo.sh dev1
```

You can also pass any pytest command line arguements, for example, just run a
single test functions:

```shell script
$ ./run-demo.sh dev1 test_01_optic_inventory.py
```

Or pass specific flags like filtering test based on test-case name:

```shell script
$ ./run-demo.sh dev1 -k "up and Eth" test_01_interface_status.py
$ ./run-demo.sh dev1 -k "up and not Eth" test_01_interface_status.py
```