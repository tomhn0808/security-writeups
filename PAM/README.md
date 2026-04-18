# PAM
PAM = Pluggable Authentication Module allows for managing authentication mechanisms in a modular way. Configuration in ```/etc/pam.d/```.
> [!WARNING]
> Try to always leave a second terminal (tty) open as root to prevent being locked out of your system. This can be achieved using ```Ctrl + Alt + F2``` in Debian for instance.

This repository primarily contains theoretical explanations and serves as a summary of PAM parameters along with brief exercise examples. For comprehensive information, the official documentation remains the most reliable resource.

## 2 types of rules in a service file:
### Management group / control / loaded module / module parameters

Example: ```auth sufficient pam_unix.so service```

### Management group / command / service

Example: ```auth include sub-service```

#### Management group (type of action, targets):

* ```auth```: verifies identity and sets up the associated credentials.

* ```account```: verifies the user account and its parameters (not linked to authentication).

* ```session```: Verifies the user session. Performs tasks for session setup/closure.

* ```password```: Verifies password validity according to the implemented policy.

#### Service rule stack 
list of rules from the same management group for a specific service.

#### Control (how to react to module success/failure):

* ```required```: Must succeed; user is notified at the end of stack processing. 1 failure = no auth, but the rest is still tested.

* ```requisite```: same as required, but if 1 failure occurs = immediately notified and therefore other modules in the stack are not executed.

* ```sufficient```: if successful, request authorized if no previous module has failed. If it fails, the module is ignored.

* ```optional```: success or failure does not matter.

#### List of modules (in /lib/x86_64-linux-gnu/security):

* ```pam_env.so```: defines environment variables specified in ```/etc/security/pam_env.conf```.

* ```pam_unix.so```: allows standard authentication.

* ```pam_securetty.so```: prohibits root login except on TTYs specified in /etc/security.

* ```pam_nologin.so```: if the ```/etc/nologin``` file exists, displays its content on any session opening attempt and prohibits login to anyone other than root. If you find that your ```/etc/nologin file``` is deleted after a reboot, this is expected behavior. The ```/etc/nologin``` file is traditionally managed by the shutdown command. When a shutdown or reboot is initiated, the system creates this file to prevent new users from logging in while the system is closing down. Once the system finishes its power cycle and starts back up, the initialization process (or the shutdown command itself) removes the file to allow normal access again.

* ```pam_deny.so```: automatically returns a failure (deny).

* ```pam_permit.so```: automatically returns a success (permit).

* ```pam_limits.so```: assigns limits to users or groups based on ```/etc/security/limits.conf```.

* ```pam_cracklib.so```: ensures the password has a sufficient security level.

* ```pam_tally.so```: locks user account based on unsuccessful login attempts.

* ```pam_time.so```: limits access times to services managed by PAM, config in /etc/security/pam.conf.

* ```pam_wheel.so```: limits access to the su command to members of the wheel group in /etc/pam.d/su.

* ```pam_mount.so```: mounts a volume for a user session.

#### Sub-service rules:

* ```@include```: include an entire stack present in another file within /etc/pam.d/.

* ```substack```: same as include except that if it fails, it does not influence the main stack.

#### ValueN = ActionN (control parameters):

* ```ValueN``` = module return values, must correspond to an ```ActionN```. In case of success, the ```ValueN``` returned by the module must correspond to an ```ActionN```.

* ```ActionN``` = action executed based on the returned ```ValueN```.

* Example: ```[success=ok new_authtok_reqd=ok ignore=ignore user_unknown=bad default=die] pam_securetty.so``` :
    * If module executes with success, pam_success value defines authentication success/failure.

    * New auth token required (example: change password at every session).
    * PAM module wants its result ignored, so it is ignored.
    * Any other results cause the stack to fail.