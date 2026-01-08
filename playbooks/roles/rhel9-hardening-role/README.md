Red Hat Enterprise Linux 9 (RHEL 9) DISA STIG (v2r1) Ansible Role
=========

This Ansible role is designed to automate the majority of the Defense Information Systems Agency (DISA) Security Technical Implementation Guides (STIGs) for Red Hat Enterprise Linux (RHEL) 9. It is built on version 2, release 1 of the RHEL 9 STIG, dated 24 April 2024. It replaces the need to use the role from RedHatOfficial's public GitHub project. It is designed specifically for RHEL 9 cloud systems and contains less than 6,000 lines of code, compared to 50,000 from the public project, making updates and maintenance far easier. Due to the high variance from environment to environment, not all STIGs can (or should) be automated. Please view the "Role Variables" section for more information.

A handful of the tasks are simply for logging or informational purposes (i.e., report if `/home` is not on a separate partition/filesystem). The playbook will log these messages on each host in a location determined by the `log_file` variable (defaults to `/tmp/rhel9-disa-stig-role.log`).

**REVIEW THE LOG FILE WHEN THE ROLE COMPLETES STIGS THAT REQUIRE MANUAL ACTION!**



Requirements
------------

This Ansible role requires Ansible v2.9 or later. Additionally, the Ansible Galaxy collections `community.general` and `ansible.posix` are required. NOTE: The collections are installed on a per-user basis; install the collection as the user that will be used to run the role! Collections can be downloaded from the Ansible Galaxy website or install the collections included in this project.

- To install the collections on Internet-connected unclassified systems:
  - `ansible-galaxy collection install community.general ansible.posix`

- To install the collections on disconnected/classified systems:
  - `ansible-galaxy collection install /path/to/community-general-8.6.0.tar.gz /path/to/ansible-posix-1.5.4.tar.gz`

Role Variables
--------------

All variables associated with this role are defined in `defaults/main.yml`. Most variables included in this role are identified by their associated STIG ID (i.e., RHEL-09-211010 is `rhel_09_211010`). Most variables are boolean and set to `true`, meaning the associated tasks in `tasks/main.yml` will be executed on the target host(s).

To disable specific STIGs for your environment, open `defaults/main.yml` in your favorite text editor and change the variable from `true` to `false`.

<details><summary>DISA CAT I STIGS (click to expand)</summary>

```
#######################################################
# DISA CAT I STIGS
#######################################################
rhel_09_211045: true # Disable systemd Ctrl-Alt-Delete burst key sequence
rhel_09_211050: true # Disable x86 Ctrl-Alt-Delete key sequence
rhel_09_214015: true # Check GPG signature of packages before installation
rhel_09_214020: true # Check GPG signature of locally install packages
rhel_09_214025: true # Enforce GPG signature verification for all software repositories
rhel_09_215015: true # Remove File Transfer Protocol (FTP) package (vsftpd)
rhel_09_215060: true # Remove Trivial File Transfer Protocol (TFTP) server package (tftp-server)
rhel_09_252070: true # Remove any shosts.equiv files found on the system
rhel_09_252075: true # Remove any .shosts files found on the system
rhel_09_255040: true # Prevent account login with empty password (ssh)
rhel_09_255050: true # Enable Pluggable Authentication Module (PAM) interface for SSHD (ssh)
rhel_09_271040: true # Prevent unattended or automatic login to system via graphical user interface
rhel_09_411100: true # (INFO ONLY) Verify only "root" account has UID "0" assignment
rhel_09_431010: true # SELinux must be in "enforcing" mode
rhel_09_672015: true # Crypto policy files must match files shipped with the operating system (crypto-policies)
```

</details>

<details><summary>DISA CAT II STIGS (click to expand)</summary>

```
#######################################################
# DISA CAT II STIGS
#######################################################
rhel_09_211020: true # Display Standard Mandatory DOD Notice and Consent Banner (/etc/issue)
rhel_09_211040: true # The systemd-journald service must be enabled
rhel_09_211055: true # Disable debug-shell service
rhel_09_212015: true # Disable ability of systemd to spawn an interactive boot process (grub)
rhel_09_212025: true # GRUB configuration file must be group-owned by root
rhel_09_212030: true # GRUB configuration file must be owned by root
rhel_09_212035: true # Disable virtual system calls (grub)
rhel_09_212040: true # Clear page allocator to prevent use-after-free attacks (grub)
rhel_09_212045: true # Clear SLUB/SLAB objects to prevent use-after-free attacks (grub)
rhel_09_213010: true # Restrict access to the kernel message buffer (sysctl)
rhel_09_213015: true # Prevent kernel profiling by nonprivileged users (sysctl)
rhel_09_213020: true # Prevent loading of a new kernel for later execution (syctl)
rhel_09_213025: true # Restrict exposed kernel pointer addresses access (sysctl)
rhel_09_213030: true # Enforce discretionary access control on hardlinks (sysctl)
rhel_09_213035: true # Enforce discretionary access control on symlinks (sysctl)
rhel_09_213040: true # Disable storing of kernel core dumps (sysctl)
rhel_09_213045: true # Disable Asynchronous Transfer Mode kernel module (modprobe.d) (requires reboot)
rhel_09_213050: true # Disable Controller Area Network kernel module (modprobe.d) (requires reboot)
rhel_09_213055: true # Disable FireWire kernel module (modprobe.d) (requires reboot)
rhel_09_213060: true # Disable Stream Control Transmission Protocol (SCTP) kernel module (modprobe.d) (requires reboot)
rhel_09_213065: true # Disable Transparent Inter Process Communication (TIPC) kernel module (modprobe.d) (requires reboot)
rhel_09_213070: true # Implement address space layout randomization (ASLR) (sysctl)
rhel_09_213075: true # Disable access to network bpf system call from nonprivileged processes (sysctl)
rhel_09_213080: true # Restrict usage of ptrace to descendant processes (sysctl)
rhel_09_213085: true # Disable core dump backtraces (coredump.conf)
rhel_09_213090: true # Disable storing core dumps (coredump.conf)
rhel_09_213095: true # Disable core dumps for all users (limits.conf)
rhel_09_213100: true # Disable acquiring, saving, and processing of core dumps
rhel_09_213105: true # Disable use of user namespaces (sysctl)
rhel_09_213110: true # Implement nonexecutable data to protect its memory from unauthorized code execution (grub)
rhel_09_213115: true # Disable kdump service
rhel_09_215010: true # The subscription-manager package must be installed
rhel_09_215020: true # The sendmail package must not be installed
rhel_09_215025: true # The nfs-utils package must not be installed
rhel_09_215030: true # The ypserv package must not be installed
rhel_09_215035: true # The rsh-server package must not be installed
rhel_09_215040: true # The telnet-server package must not be installed
rhel_09_215045: true # The gssproxy package must not be installed
rhel_09_215050: true # The iprutils package must not be installed
rhel_09_215055: true # The tuned package must not be installed
rhel_09_215065: true # The quagga package must not be installed
rhel_09_215075: true # The openssl-pkcs11 package must be installed
rhel_09_215080: true # The gnutls-utils package must be installed
rhel_09_215085: true # The nss-tools package must be installed
rhel_09_215090: true # The rng-tools package must be installed
rhel_09_215095: true # The s-nail package must be installed
rhel_09_231040: true # Disable autofs service
rhel_09_232010: true # System commands must have mode 0755 or less permissive
rhel_09_232015: true # Library directories must have mode 0755 or less permissive
rhel_09_232020: true # Library files must have mode 0755 or less permissive
rhel_09_232025: true # /var/log directory must have mode 0755 or less permissive
rhel_09_232030: true # /var/log/messages file must have mode 0640 or less permissive
rhel_09_232035: true # Audit tools must have mode 0755 or less permissive
rhel_09_232040: true # Cron configuration directories must have mode 0700 or less permissive
rhel_09_232045: true # Local user initialization files must have mode 0740 or less permissive
rhel_09_232050: true # Local user home directories must have mode 0750 or less permissive
rhel_09_232055: true # /etc/group file must have mode 0644 or less permissive
rhel_09_232060: true # /etc/group- file must have mode 0644 or less permissive
rhel_09_232065: true # /etc/gshadow file must have mode 0000 or less permissive
rhel_09_232070: true # /etc/gshadow- file must have mode 0000 or less permissive
rhel_09_232075: true # /etc/passwd file must have mode 0644 or less permissive
rhel_09_232080: true # /etc/passwd- file must have mode 0644 or less permissive
rhel_09_232085: true # /etc/shadow- file must have mode 0000 or less permissive
rhel_09_232090: true # /etc/group file must be owned by root
rhel_09_232095: true # /etc/group file must be group-owned by root
rhel_09_232100: true # /etc/group- file must be owned by root
rhel_09_232105: true # /etc/group- file must be group-owned by root
rhel_09_232110: true # /etc/gshadow file must be owned by root
rhel_09_232115: true # /etc/gshadow file must be group-owned by root
rhel_09_232120: true # /etc/gshadow- file must be owned by root
rhel_09_232125: true # /etc/gshadow- file must be group-owned by root
rhel_09_232130: true # /etc/passwd file must be owned by root
rhel_09_232135: true # /etc/passwd file must be group-owned by root
rhel_09_232140: true # /etc/passwd- file must be owned by root
rhel_09_232145: true # /etc/passwd- file must be group-owned by root
rhel_09_232150: true # /etc/shadow file must be owned by root
rhel_09_232155: true # /etc/shadow file must be group-owned by root
rhel_09_232160: true # /etc/shadow- file must be owned by root
rhel_09_232165: true # /etc/shadow- file must be group-owned by root
rhel_09_232170: true # /var/log directory must be owned by root
rhel_09_232175: true # /var/log directory must be group-owned by root
rhel_09_232180: true # /var/log/messages file must be owned by root
rhel_09_232185: true # /var/log/messages file must be group-owned by root
rhel_09_232190: true # System commands must be owned by root
rhel_09_232195: true # System commands must be group-owned by root
rhel_09_232200: true # Library files must be owned by root
rhel_09_232205: true # Library files must be group-owned by root
rhel_09_232210: true # Library directories must be owned by root
rhel_09_232215: true # Library directories must be group-owned by root
rhel_09_232220: true # Audit tools must be owned by root
rhel_09_232225: true # Audit tools must be group-owned by root
rhel_09_232230: true # Cron configuration files and directories must be owned by root
rhel_09_232235: true # Cron configuration files and directories must be group-owned by root
rhel_09_232245: true # Sticky bit must be set on all world-writable directories
rhel_09_232250: true # Local files and directories must have a valid group owner
rhel_09_232255: true # Local files and directories must have a valid owner
rhel_09_232265: true # /etc/crontab file must have mode 0600
rhel_09_232270: true # /etc/shadow file must have mode 0000
rhel_09_251010: true # The firewalld package must be installed
rhel_09_251015: true # The firewalld service must be active
rhel_09_251030: true # Configure nftables to allow rate limits on any connection to the system (firewalld.conf)
rhel_09_251045: true # Enable hardening for the Berkeley Packet Filter just-in-time compiler (sysctl)
rhel_09_252010: true # The chrony package must be installed
rhel_09_252015: true # The chronyd service must be enabled
rhel_09_252040: true # Configure DNS mode in Network Manager (NetworkManager.conf)
rhel_09_252045: true # Unauthorized IP tunnels must not be configured (ipsec)
rhel_09_252050: true # Prevent unrestricted mail relaying (postconf)
rhel_09_252060: true # Forward mail from postmaster to the root account using a postfix alias (/etc/aliases)
rhel_09_252065: true # The libreswan package must be installed
rhel_09_253010: true # Use TCP syncookies (sysctl)
rhel_09_253015: true # Ignore IPv4 ICMP redirect messages (sysctl)
rhel_09_253020: true # Do not forward IPv4 source-routed packets (sysctl)
rhel_09_253025: true # Log IPv4 packets with impossible addresses (sysctl)
rhel_09_253030: true # Log IPv4 packets with impossible addresses by default (sysctl)
rhel_09_253035: true # Use reverse path filtering on all IPv4 interfaces (sysctl)
rhel_09_253040: true # Prevent IPv4 redirect messages from being accepted (syctl)
rhel_09_253045: true # Do not forward IPv4 source-routed packets by default (sysctl)
rhel_09_253050: true # Use reverse-path filter for IPv4 network traffic when possible by default (sysctl)
rhel_09_253055: true # Do not respond to ICMP echos sent to a broadcast address (syctl)
rhel_09_253060: true # Limit the number of bogus ICMP response errors logs (sysctl)
rhel_09_253065: true # Do not send ICMP redirects (sysctl)
rhel_09_253070: true # Do not allow ICMP redirects by default (sysctl)
rhel_09_253075: true # Do not enable IPv4 packet forwarding unless the system is a router (sysctl)
rhel_09_254010: true # Do not accept router advertisements on all IPv6 interfaces (sysctl)
rhel_09_254015: true # Ignore IPv6 ICMP redirect messages (sysctl)
rhel_09_254020: true # Do not forward IPv6 source-routed packets (sysctl)
rhel_09_254025: true # Do not enable IPv6 packet forwarding unless the system is a router (sysctl)
rhel_09_254030: true # Do not accept router advertisements on all IPv6 interfaces by default (sysctl)
rhel_09_254035: true # Prevent IPv6 ICMP redirect messages from being accepted (sysctl)
rhel_09_254040: true # Do not forward IPv6 source-routed packets by default (sysctl)
rhel_09_255010: true # The openssh-server package must be installed
rhel_09_255015: true # The sshd service must be active and enabled
rhel_09_255020: true # The openssh-clients package must be installed
rhel_09_255025: true # Display Standard Mandatory DOD Notice and Consent Banner (ssh)
rhel_09_255030: true # Log SSH connection attempts and failures (ssh)
rhel_09_255035: true # SSH must accept public key authentication (ssh)
rhel_09_255045: true # Do not permit direct logons to the root account (ssh)
rhel_09_255055: true # SSH daemon must use system-wide crypto policies (ssh)
rhel_09_255060: true # SSH client connections must implement DOD-approved encryption ciphers (ssh)
rhel_09_255065: true # Implement DOD-approved encryption ciphers to protect confidentiality of SSH server connections (crypto-policies)
rhel_09_255075: true # Configure SSH server to use only MACs employing FIPS 140-3 validated cryptographic hash algorithms (crypto-policies)
rhel_09_255080: true # Do not allow a noncertificate trusted host SSH logon to the system (ssh)
rhel_09_255085: true # Do not allow users to overwrite SSH environment variables (ssh)
rhel_09_255090: true # Force frequent session key renegotiation (ssh)
rhel_09_255095: true # Terminate SSH traffic after becoming unresponsive (ssh)
rhel_09_255100: true # Terminate SSH traffic after 10 minutes of becoming unresponsive (ssh)
rhel_09_255105: true # SSH configuration file must be group-owned by root (ssh)
rhel_09_255110: true # SSH configuration file must be owned by root (ssh)
rhel_09_255115: true # SSH configuration file must have mode 0600 or less permissive (ssh)
rhel_09_255120: true # SSH private host key files must have mode 0640 or less permissive
rhel_09_255125: true # SSH public host key files must have mode 0644 or less permissive
rhel_09_255130: true # SSH daemon must not allow compression or only allow compression after successful authentication (ssh)
rhel_09_255135: true # SSH daemon must not allow GSSAPI authentication (ssh)
rhel_09_255140: true # SSH daemon must not allow Kerberos authentication (ssh)
rhel_09_255145: true # SSH daemon must not allow rhosts authentication (ssh)
rhel_09_255150: true # SSH daemon must not allow known hosts authentication (ssh)
rhel_09_255155: true # SSH daemon must disable remote X connections for interactive users (ssh)
rhel_09_255160: true # SSH daemon must perform strict mode checking of home directory configuration files (ssh)
rhel_09_255165: true # SSH daemon must display the date and time of the last successful account logon (ssh)
rhel_09_255170: true # SSH daemon must be configured to use privilege separation (ssh)
rhel_09_255175: true # SSH daemon must prevent remote hosts from connecting to the proxy display (ssh)
rhel_09_271010: true # Display Standard Mandatory DOD Notice and Consent Banner (GUI)
rhel_09_271015: true # Prevent users from overriding banner message (GUI)
rhel_09_271020: true # Disable graphical user interface automount function (GUI)
rhel_09_271025: true # Prevent users from overriding automount function (GUI)
rhel_09_271030: true # Disable graphical user interface autorun function (GUI)
rhel_09_271035: true # Prevent users from overriding graphical user interface autorun function (GUI)
rhel_09_271045: true # Lock sessions for all connection types using smart card when it is removed (GUI)
rhel_09_271050: true # Prevent users from overriding smart card removal action (GUI)
rhel_09_271055: true # Lock sessions until users reauthenticate (GUI)
rhel_09_271060: true # Prevent users from overriding screensaver session lock (GUI)
rhel_09_271065: true # Lock sessions after 15 minutes of inactivity (GUI)
rhel_09_271070: true # Prevent users from overriding session inactivity lock (GUI)
rhel_09_271075: true # Lock sessions when screensaver is activated (GUI)
rhel_09_271080: true # Prevent users from overriding session lock delay (GUI)
rhel_09_271085: true # Conceal information previously visible on display with session lock (GUI)
rhel_09_271090: true # Effective dconf policy must match policy keyfiles (GUI)
rhel_09_271095: true # Disable ability to reboot from the login screen (GUI)
rhel_09_271100: true # Prevent users from overriding reboot from login screen setting (GUI)
rhel_09_271105: true # Disable Ctrl-Alt-Del reboot/shut down action (GUI)
rhel_09_271110: true # Prevent users from overriding Ctrl-Alt-Del reboot/shut down action (GUI)
rhel_09_271115: true # Disable user list at logon (GUI)
rhel_09_291010: true # Disable USB mass storage kernel module (modprobe.d) (requires reboot)
rhel_09_291015: true # The usbguard package must be installed
rhel_09_291020: true # The usbguard service must be enabled
rhel_09_291035: true # Disable Bluetooth kernel module (modprobe.d) (requires reboot)
rhel_09_411010: true # Passwords for new users & password changes must have 60-day maximum lifetime (login.defs)
rhel_09_411015: true # User account passwords must have a 60-day maximum lifetime restriction (exclude system accounts)
rhel_09_411020: true # Local interactive user accounts must be assigned a home directory at creation (login.defs)
rhel_09_411025: true # Remove any overrides of UMASK in all local interactive user initialization files
rhel_09_411050: true # Disable account identifiers (users, groups, roles, & devices) after 35 days of inactivity (useradd)
rhel_09_411095: true # Unauthorized/unnecessary accounts must not be present (games & gopher)
rhel_09_411115: true # Local user initialization files must not execute world-writable programs
rhel_09_412035: true # Automatically exit interactive command shell user sessions after 15 minutes of inactivity (tmout.sh)
rhel_09_412050: true # Enforce a delay of at least four seconds after a failed logon attempt (login.defs)
rhel_09_412055: true # Define default permissions (UMASK) for the bash shell (/etc/bashrc)
rhel_09_412060: true # Define default permissions (UMASK) for the c shell (/etc/csh.cshrc)
rhel_09_412065: true # Set the UMASK value to 077 for all local interactive user accounts (login.defs)
rhel_09_412070: true # Define default permissions (UMASK) for the system default profile (/etc/profile)
rhel_09_412080: true # Terminate sessions that have been idle for 15 minutes, but preserve tmux sessions (logind.conf)
rhel_09_431015: true # The SELinux targeted policy must be enabled (/etc/selinux/config)
rhel_09_431025: true # The policycoreutils package must be installed
rhel_09_431030: true # The policycoreutils-python-utils package must be installed
rhel_09_432010: true # The sudo package must be installed
rhel_09_432015: true # Require reauthentication when using "sudo" command
rhel_09_432020: true # Force invoking of user's password for privilege escalation when using "sudo"
rhel_09_432025: true # Require users to reauthenticate for privilege escalation (sudo)
rhel_09_432030: true # Restrict privilege escalation to authorized personnel (sudo)
rhel_09_433010: true # The fapolicyd package must be installed
rhel_09_611060: true # Enforce password complexity rules for the root account (pwquality.conf)
rhel_09_611065: true # Require at least one lowercase character in passwords (pwquality.conf)
rhel_09_611070: true # Require at least one numeric character in passwords (pwquality.conf)
rhel_09_611075: true # Passwords for new users & password changes must have 24-hour minimum lifetime (login.defs)
rhel_09_611080: true # Passwords must have a 24-hour minimum lifetime restriction in /etc/shadow
rhel_09_611085: true # Require users to provide a password for privilege escalation (sudo/NOPASSWD)
rhel_09_611090: true # Require at least 15 characters in passwords (pwquality.conf)
rhel_09_611095: true # Passwords for new users must have a minimum of 15 characters (login.defs)
rhel_09_611100: true # Require at least one special character in passwords (pwquality.conf)
rhel_09_611105: true # Prevent use of dictionary words in passwords (pwquality.conf)
rhel_09_611110: true # Require at least one uppercase character in passwords (pwquality.conf)
rhel_09_611115: true # Require change of at least eight characters when passwords are changed (pwquality.conf)
rhel_09_611120: true # Enforce maximum of four repeating characters of the same class when passwords are changed (pwquality.conf)
rhel_09_611125: true # Enforce maximum of three repeating characters when passwords are changed (pwquality.conf)
rhel_09_611130: true # Require change of at least four character classes when passwords are changed (pwquality.conf)
rhel_09_611135: true # Account administration utilities must be configured to store only encrypted repesentations of passwords (libuser.conf)
rhel_09_611140: true # Ensure shadow file stores only encrypted representations of passwords (login.defs)
rhel_09_611150: true # Shadow password suite must use sufficient number of hashing rounds (login.defs)
rhel_09_611155: true # Lock accounts that have blank or null passwords in /etc/shadow
rhel_09_611160: true # The CAC smart card driver must be in use (if opensc is installed) (/etc/opensc.conf)
rhel_09_611175: true # The pcsc-lite package must be installed
rhel_09_611180: true # The pcscd service must be active and enabled
rhel_09_611185: true # The opensc package must be installed
rhel_09_611195: true # Require authentication to access emergency mode
rhel_09_611200: true # Require authentication to access single-user mode
rhel_09_652010: true # The rsyslogd package must be installed
rhel_09_652015: true # The rsyslog-gnutls package must be installed
rhel_09_652020: true # The rsyslog service must be active
rhel_09_652030: true # All remote access methods must be monitored (rsyslog.conf)
rhel_09_652035: true # Audit records must be offloaded onto a different system (syslog.conf)
rhel_09_652060: true # Logging of cron must be enabled (rsyslog.conf)
rhel_09_653010: true # The audit package must be installed
rhel_09_653015: true # The audit service must be enabled (auditd)
rhel_09_653020: true # Configure auditd to SYSLOG when an error writing to the audit storage volume occurs (auditd.conf)
rhel_09_653025: true # Configure auditd to SYSLOG when the audit storage volume is full (auditd.conf)
rhel_09_653035: true # Configure auditd to take action when audit storage volume reaches 75 percent capacity (auditd.conf)
rhel_09_653040: true # Configure auditd to notify the SA and ISSO (at a minimum) when audit storage volume reaches 75 percent capacity (auditd.conf)
rhel_09_653045: true # Configure auditd to take action when audit storage volume reaches 95 percent capacity (auditd.conf)
rhel_09_653050: true # Configure auditd to enter single-user mode when audit storage volume reaches 95 percent capacity (auditd.conf)
rhel_09_653055: true # Configure auditd to ROTATE logs when the audit files have reached maximum size (auditd.conf)
rhel_09_653060: true # Configure auditd to label all offloaded audit logs before sending them to the central log server (auditd.conf)
rhel_09_653065: true # Configure auditd to syslog when the internal event queue is full (auditd.conf)
rhel_09_653070: true # Configure auditd to alert the SA and ISSO (at a minimum) when an audit processing failure event occurs (auditd.conf)
rhel_09_653075: true # Configure auditd to audit local events (auditd.conf)
rhel_09_653080: true # Audit logs must be group-owned by root
rhel_09_653085: true # /var/log/audit directory must be owned by root
rhel_09_653090: true # Audit logs must have mode 0600 or less permissive
rhel_09_653095: true # Configure auditd to periodically flush audit records to prevent the loss of audit records (auditd.conf)
rhel_09_653100: true # Configure auditd to use ENRICHED log formatting (auditd.conf)
rhel_09_653105: true # Configure auditd to write audit records to disk (auditd.conf)
rhel_09_653115: true # /etc/audit/auditd.conf must have mode '0640' or less permissive
rhel_09_653130: true # The audispd-plugins package must be installed
rhel_09_671015: true # Lock accounts that have insecure password hashes (SHA-512 is required) (/etc/shadow)
rhel_09_671020: true # Configure Libreswan to use the system cryptographic policy (ipsec.conf)
rhel_09_672010: true # The crypto-policies package must be installed
rhel_09_672020: true # Prevent override of system crypto policies (crypto-policies)
rhel_09_672025: true # Configure Kerberos to use system crypto policy (crypto-policies)
rhel_09_672035: true # Configure OpenSSL library to use system crypto policy (openssl.cnf)
rhel_09_672040: true # Configure OpenSSL library to use only DOD-approved TLS encryption (crypto-policies)
rhel_09_672050: true # Configure BIND (if installed) to use system crypto policy (named.conf)
```
</details>

<details><summary>DISA CAT III STIGS (click to expand)</summary>

```
#######################################################
# DISA CAT III STIGS
#######################################################
rhel_09_212050: true # Enable mitigations against processor-based vulnerabilities (grub)
rhel_09_212055: true # Enable auditing of processes that start prior to the audit daemon (grub)
rhel_09_214035: true # Remove all software components after updated versions have been installed
rhel_09_231195: true # Disable cramfs kernel module (modprobe.d) (requires reboot)
rhel_09_252025: true # Disable chrony daemon from acting as a server (chrony.conf)
rhel_09_252030: true # Disable network management of the chrony daemon (chrony.conf)
rhel_09_291025: true # Audit logging must be enabled for the USBGuard daemon
rhel_09_412040: true # Limit the number of concurrent sessions to 10 for all accounts
rhel_09_653120: true # Allocate an audit backlog limit of sufficient size (grub)
```

</details>

<details><summary>Pluggable Authentication Module (PAM) STIGS (click to expand)</summary>

```
#######################################################
# PAM STIGS
#######################################################
# The following task deploys fully STIGed pam.d files (password-auth-local, system-auth-local, postlogin-local, su, & sudo).
# It satisfies CAT I RHEL-09-611025.
# It satisfies CAT II's RHEL-09-432035, RHEL-09-611010, RHEL-09-611030, RHEL-09-611035,
#   RHEL-09-611040, RHEL-09-611045, RHEL-09-611050, RHEL-09-611055, RHEL-09-611145, & RHEL-09-671025.
# It satisfies CAT III RHEL-09-412075.
pam_stig_files: true
# This task deploys a fully STIGed config file in /etc/security/faillock.conf.
# It also creates a non-default faillock tally directory at /var/log/faillock, sets appropriate SELinux contexts, and creates an SELinux rule.
# It satisfies CAT II's RHEL-09-411075, RHEL-09-411080, RHEL-09-411085, RHEL-09-411090, RHEL-09-411105, RHEL-09-412045, & RHEL-09-431020.
pam_faillock: true
```

</details>

<details><summary>Audit Rules STIGS (click to expand)</summary>

```
#######################################################
# AUDIT RULES STIGS
#######################################################
# The following task removes any existing audit rules and replaces them with fully STIG'ed audit rule files (01-audit.rules & 99-finalize.rules).
# It satisfies a large amount of STIGs.
audit_rules: true
```

</details>

<details><summary>Role Logging (click to expand)</summary>

```
#######################################################
# ROLE LOGGING
#######################################################
# Log file to store findings for STIGs that require manual administrator action.
log_file: /tmp/rhel9-disa-stig-role.log
# Initialize log variable to store STIG findings.
log_var: [] # The brackets define this variable as a list type.
```

</details>

<details><summary>FIPS (click to expand)</summary>

```
#######################################################
# ENABLE FIPS
#######################################################
# The following task enables FIPS mode.
# It satisfies CAT I's RHEL-09-671010 & RHEL-09-672030.
# It satisfies CAT II RHEL-09-672045.
fips_enable: true
```

</details>

<details><summary>TMUX (click to expand)</summary>

```
#######################################################
# TMUX CONFIGURATION
#######################################################
# There are fix total STIGs related to tmux: four CAT II's and one CAT III.
# CAT II TMUX STIGS
rhel_09_412010: true # The tmux package must be installed
rhel_09_412015: true # Initialize the tmux terminal multiplexer as each shell is called (/etc/profile.d/tmux.sh)
tmux_config: true # Enable user session lock and 15 minute timeout (tmux) (Satisfies CAT II's RHEL-09-412020 & RHEL-09-412025)
# CAT III TMUX STIGS
rhel_09_412030: true # Prevent users from disabling the tmux terminal multiplexer (/etc/shells)
```

</details>

<details><summary>AIDE (click to expand)</summary>

```
#######################################################
# AIDE STIGS
#######################################################
# The following tasks installs aide, creates a daily cronjob, & deploys a fully STIGed aide configuration file (aide.conf).
# It satisfiles CAT II's RHEL-09-651010, RHEL-09-651015, RHEL-09-651020, & RHEL-09-651025
# It satisfies CAT III's RHEL-09-651030 & RHEL-09-651035
# IMPORTANT! Ensure you update the "aide_email" variable with email address that is monitored by security and/or sysadmin personnel!
aide_email: root # REPLACE this variable with the email address used to receive aide integrity reports
aide_conf: true # Deploy fully STIGed aide configuration file (aide.conf)
```

</details>

<details><summary>Manual STIGs (click to expand)</summary>

```
#######################################################
# MANUAL STIGS
#######################################################
# The following STIGs should either be completed manually or with an Ansible playbook/role that is customized for the target environment.
# RHEL-09-211010 (CAT I): RHEL 9 must be a vendor-supported release (not a finding for systems that are kept up to date)
# RHEL-09-231190 (CAT I): Configure encryption at rest for every persistent disk partition (LUKS)
# RHEL-09-211015 (CAT II): System security patches and updates must be installed and up to date
# RHEL-09-211030 (CAT II): The graphical display manager must not be the default target unless approved (GUI)
# RHEL-09-215070 (CAT II): A graphical display manager must not be installed unless approved
# RHEL-09-251025 (CAT II): Configure firewalld to allow approved settings and/or running services to comply with the PPSM CLSA for the sit or program and the PPSM CAL
# RHEL-09-251035 (CAT II): Configure firewalld to prohibit/restrict use of functions, ports, protocols, and/or services as defined in the PPSM CAL and vulnerability assessments
# RHEL-09-252020 (CAT II): Configure chrony to securely compare internal clocks at least every 24 hours with an NTP server (chrony.conf)
# RHEL-09-291030 (CAT II): Unauthorized peripherals must be blocked (usbguard); not common in cloud environments
# RHEL-09-411055 (CAT II): PATH environment variable in user local initialization files must only contain paths to the system default or the user's home directory
# RHEL-09-411070 (CAT II): Local interactive user home directories must be group-owned by the owner's primary group
# RHEL-09-433015 (CAT II): fapolicy module must be enabled; requires extensive custom configuration
# RHEL-09-611165 (CAT II): Enable certificate based smart card authentication
# RHEL-09-611170 (CAT II): Implement certificate status checking for multifactor authentication (sssd)
# RHEL-09-611190 (CAT II): All SSH private keys must have a passcode
# RHEL-09-631010 (CAT II): Certificates must be validated for PKI-based authentication (sssd)
# RHEL-09-631015 (CAT II): Authenticated identities must be maped to the user or group for PKI-based authentication (sssd)
# RHEL-09-631020 (CAT II): Prohibit the use of cached authenticators after one day (sssd)
# RHEL-09-653125 (CAT II): Mail aliases must be configured to notify the ISSO and SA (at a minimum) in the event of an audit processing failure
```

</details>

<details><summary>Informational Only STIGs (click to expand)</summary>

```
#######################################################
# INFORMATIONAL ONLY
#######################################################
# CAT II INFORMATIONAL STIGS
rhel_09_214010: true # (INFO ONLY) Red Hat package-signing keys must be installed and match published values
rhel_09_214030: true # (INFO ONLY) Cryptographic hashes of system files must match vendor values
rhel_09_215070: true # (INFO ONLY) A graphical display manager must not be installed unless approved
rhel_09_231010: true # (INFO ONLY) /home directory must be mounted on a separate filesystem/partition
rhel_09_231015: true # (INFO ONLY) /tmp directory must be mounted on a separate filesystem/partition
rhel_09_231035: true # (INFO ONLY) /var/tmp directory must be mounted on a separate filesystem/partition
rhel_09_231045: true # (INFO ONLY) /home must be mounted with the "nodev" option
rhel_09_231050: true # (INFO ONLY) /home must be mounted with the "nosuid" option
rhel_09_231055: true # (INFO ONLY) /home must be mounted with the "noexec" option
rhel_09_231060: true # (INFO ONLY) NFS mounts must be configured to use RPCSEC_GSS (sec=krb5p:krb5i:krb5)
rhel_09_231065: true # (INFO ONLY) NFS mounts must be mounted with the "nodev" option
rhel_09_231070: true # (INFO ONLY) NFS mounts must be mounted with the "noexec" option
rhel_09_231075: true # (INFO ONLY) NFS mounts must be mounted with the "nosuid" option
rhel_09_231095: true # (INFO ONLY) /boot must be mounted with the "nodev" option
rhel_09_231100: true # (INFO ONLY) /boot must be mounted with the "nosuid" option
rhel_09_231105: true # (INFO ONLY) /boot/efi must be mounted with the "nosuid" option
rhel_09_231110: true # (INFO ONLY) /dev/shm must be mounted with the "nodev" option
rhel_09_231115: true # (INFO ONLY) /dev/shm must be mounted with the "noexec" option
rhel_09_231120: true # (INFO ONLY) /dev/shm must be mounted with the "nosuid" option
rhel_09_231125: true # (INFO ONLY) /tmp must be mounted with the "nodev" option
rhel_09_231130: true # (INFO ONLY) /tmp must be mounted with the "noexec" option
rhel_09_231135: true # (INFO ONLY) /tmp must be mounted with the "nosuid" option
rhel_09_231140: true # (INFO ONLY) /var must be mounted with the "nodev" option
rhel_09_231145: true # (INFO ONLY) /var/log must be mounted with the "nodev" option
rhel_09_231150: true # (INFO ONLY) /var/log must be mounted with the "noexec" option
rhel_09_231155: true # (INFO ONLY) /var/log must be mounted with the "nosuid" option
rhel_09_231160: true # (INFO ONLY) /var/log/audit must be mounted with the "nodev" option
rhel_09_231165: true # (INFO ONLY) /var/log/audit must be mounted with the "noexec" option
rhel_09_231170: true # (INFO ONLY) /var/log/audit must be mounted with the "nosuid" option
rhel_09_231175: true # (INFO ONLY) /var/tmp must be mounted with the "nodev" option
rhel_09_231180: true # (INFO ONLY) /var/tmp must be mounted with the "noexec" option
rhel_09_231185: true # (INFO ONLY) /var/tmp must be mounted with the "nosuid" option
rhel_09_231200: true # (INFO ONLY) Non-root local partitions must be mounted with the "nodev" option
rhel_09_232240: true # (INFO ONLY) World-writable directories must be owned by root, sys, bin, or an application user
rhel_09_232260: true # (INFO ONLY) System device files must be correctly labeled (SELinux)
rhel_09_251020: true # (INFO ONLY) System firewall must employ a deny-all, allow-by-exception policy (firewalld)
rhel_09_251040: true # (INFO ONLY) Network interfaces must not be in promiscuous mode
rhel_09_252035: true # (INFO ONLY) DNS resolution must have at least two name servers configured
rhel_09_252055: true # (INFO ONLY) TFTP server daemon (if required) must operate in secure mode (tftp-server)
rhel_09_411030: true # (INFO ONLY) Duplicate user IDs (UIDs) must not exist for interactive users
rhel_09_411035: true # (INFO ONLY) System accounts must not have an interactive login shell
rhel_09_411045: true # (INFO ONLY) Interactive users must have a primary group that exists (pwck)
rhel_09_411060: true # (INFO ONLY) All local interactive users must have a home directory assigned in the /etc/passwd file
rhel_09_411065: true # (INFO ONLY) All local interactive user home directories defined in /etc/passwd must exist
rhel_09_411110: true # (INFO ONLY) Groups must have unique group IDs (GIDs) (/etc/group)
rhel_09_611205: true # (INFO ONLY) System daemons must be prevented from using Kerberos for authentication
rhel_09_652025: true # (INFO ONLY) The rsyslog daemon must not accept log messages from other servers unless it is being used for log aggregation
rhel_09_652040: true # (INFO ONLY) Remote logging servers for offloading audit logs via rsyslog must be encrypted (DriverAuthMode) (rsyslog.conf)
rhel_09_652045: true # (INFO ONLY) Remote logging servers for offloading audit logs via rsyslog must be encrypted (DriverMode) (rsyslog.conf)
rhel_09_652050: true # (INFO ONLY) Remote logging servers for offloading audit logs via rsyslog must be encrypted (DefaultNetstreamDriver) (rsyslog.conf)
rhel_09_652055: true # (INFO ONLY) Audit records must be forwarded via TCP to a remote logging server or separate storage media (rsyslog.conf)
rhel_09_653030: true # (INFO ONLY) Audit record storage capacity must be sufficient to store at least one week's worth of audit records
# CAT III INFORMATIONAL STIGS
rhel_09_231020: true # (INFO ONLY) /var directory must be mounted on a separate filesystem/partition
rhel_09_231025: true # (INFO ONLY) /var/log directory must be mounted on a separate filesystem/partition
rhel_09_231030: true # (INFO ONLY) /var/log/audit directory must be mounted on a separate filesystem/partition
```

</details>

<details><summary>STIGs Not Applicable (click to expand)</summary>

```
#######################################################
# STIGS NOT APPLICABLE
#######################################################
# The following STIGs have been determined to not be applicable to the latest RHEL 9 release in a cloud environment.
# RHEL-09-213105 (CAT II): Disable the use of user namespaces (sysctl) (N/A if containers are in use; MANUAL if system does not use containers)
# RHEL-09-231080 (CAT II): Removable media must be mounted with the "noexec" option (typically N/A for virtual systems)
# RHEL-09-231085 (CAT II): Removable media must be mounted with the "nodev" option (typically N/A for virtual systems)
# RHEL-09-231090 (CAT II): Removable media must be mounted with the "nosuid" option (typically N/A for virtual systems)
# RHEL-09-291040 (CAT II): Wireless network adapters must be disabled (N/A for systems that do not have physical wireless network adapters)
# RHEL-09-411040 (CAT II): Temporary accounts must automatically expire within 72 hours (not common)
# RHEL-09-211035 (CAT III): Start and enable rngd service (N/A for RHEL 9 running in FIPS mode)
```

</details>

How to Run the Role
-------------------

This role can be run from an Ansible control node or on the local host. You simply run the `start-rhel9-disa-stig-role.yml` playbook.

- On Ansible control node:
  - `ansible-playbook -i /path/to/inventory --limit <HOST_GROUP or HOST_NAME> /path/to/start-rhel9-disa-stig-role.yml`
    - Common arguments:
      - `-u`: username on target host(s) (if different than current user)
      - `-k`: prompt for SSH password
      - `-K`: prompt for sudo or dzdo password for privelege escalation

- On local host:
  - Download and extract tarball or ZIP archive of the project code.
  - Change into the extracted directory.
  - Change the `hosts: all` to `hosts: localhost` in `start-rhel9-disa-stig-role.yml`.
  - `ansible-playbook start-rhel9-disa-stig-role.yml`