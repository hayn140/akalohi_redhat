dnf_update
=========

This will: 
- Unset the release version in case it's limited via activation key.
- Drop all extra repos.
- Update the server and reboot it if needed.

Vars
------------
```
# 'null' will unset the release, we can also change it 
# to something like '8.9', '9.3', etc.
target_release: 'null'
```

Dependencies
------------

Server already connected to repos  


Author Information
------------------

Agmill3 is an elder millennial