Install Wireshark and libpcap:

**sudo apt-get install wireshark libpcap0.8**

For Debian, Ubuntu and other Debian derivatives, continue to step 3.

For other Linux based systems or other installation methods, see the Wireshark Wiki, then go to step 6.

Reconfigure wireshark to allow non-superusers to track packets:

**sudo dpkg-reconfigure wireshark-common**

Select <Yes> in the prompt

Add your username to the "wireshark" usergroup:

**sudo usermod -a -G wireshark <your_username>**

You can verify if it’s done correctly by displaying the groups your username is part of:

groups <your_username>

If not, you can add the group "wireshark" manually:

**groupadd wireshark**

And then add your username to the group (see above)

Important: Logout of your session, then log back in.

This step depends on the kernel version that is installed on your machine. To know the version of your kernel, type:

**uname -r**

For versions of the kernel prior to 2.6.21, if debugfs is not already mounted on /sys/kernel/debug, ensure that it is mounted there by issuing the following command:

**sudo mount -t debugfs / /sys/kernel/debug**

For kernel version 2.6.21 and later, load the loadable module usbmon in the Kernel:

**sudo modprobe usbmon**

See Wireshark Wiki for more information about this differentiation.

If the usbmon interfaces don't appear in Wireshark, look for interfaces using dumpcap (the command-line tool of Wireshark):

**sudo dumpcap -D**

You should see the usbmon* interfaces. Now display the permissions of the usbmon interfaces:

**ls -l /dev/usbmon***

If the usbmon* files have 'crw-------', then it's normal that Wireshark cannot read them because it's not run as root. Do not execute wireshark in root mode, it may damage files. Instead, you can give it regular users privileges :

**sudo setfacl -m u:$USER:r /dev/usbmon***