# Example Live DUT Testing

In order to connect to your remote devices, you will need to export the
following environment variables:

```bash
export EOS_USER=your-login-name
export EOS_PASSWORD=your-login-password
```

If you are using an ssh-config file for hostname resolution (i.e. no DNS), you
will also need to:

```bash
export EOS_SSH_CONFIG=<path-to-ssh-config file>
```

# Snapshot Live DUT

In order to automatically create test-cases based on the existing operational states, you can
use the `nrfu-snapshot.py` program.  For exmaple:

```bash
./nrfu-snapshot.py switch-101.bld1
```

You can provide either the hostname (as shown) or the IP address of the device.  Note that which every
you use, you must ensure that the EOS device is configured to support eAPI. 

Once you run this utility, you will see the following output indicating information about
each of test functions.  For example, running the command:

````bash
$ ./nrfu-snapshot.py switch-101.bld1
````

Will result in the following output
```bash
Ensure directory: switch-101.bld1
	[+] test-cabling creating 6 test-cases
	[+] test-lag-status creating 5 test-cases
	[+] test-interface-status creating 73 test-cases
	[+] test-optic-inventory creating 60 test-cases
	[+] test-mlag-status creating 1 test-cases
	[+] test-mlag-interface-status creating 4 test-cases
````

You should see the new directory `switch-101.bld1`, and inside there a number of JSON files storing
the test-cases for each of the test functions, for example `switch-101.bld1/test_optic_inventory.json`

# Run NRFU Tests

Once you have your test-cases created, you can then run the NRFU test utility:

For example using the same "switch-101.bld1" host:

````bash
./nrfu-dev.sh switch-101.bld1
````

The shell-script is a wrapper around calling pytest, and you should see as the first line in the output 
something like this:

```bash
+ pytest -v --tb=no --html=switch-101.bld1/report.html \
    --nrfu-device switch-101.bld1 \
    --nrfu-testcasedir switch-101.bld1
```

And then following that, the output of the pytest execution.  The pytest run will generate an HTML report
file that you can use to see details of each of the failed tests.  You can open that report file in your
browswer window directly