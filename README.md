# About

This tiny project, fastboot-tcp2serial, relays fastboot protocol to originally unsupported serial interfaces.

It is Developed with Python 3.8.1 under Windows 7.

Its goal is to let UART based small embedded systems (without ethernet and USB port) able to leverage the utilities provided by Android ecosystem.

# Prerequisites

pip --trusted-host pypi.org --trusted-host files.pythonhosted.org -v install pyserial parse

# Hand-on

With a file "xxxxx.bin" for trial.

1. Run with "python.exe fb2ser.py"
2. Run fastboot with "fastboot -s tcp:127.0.0.1:5005 flash pp xxxxx.bin"

# TODO

1. Support actual serial port.
2. Support options to show available serial ports.
3. Support options to select TCP port number.

# References

1. [fastboot](https://android.googlesource.com/platform/system/core/+/refs/heads/master/fastboot/)

