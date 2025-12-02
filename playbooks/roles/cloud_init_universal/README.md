cloud_init_universal
=========

This will: 
- Copy out a cloud init based on what the var 'cloud_provider' is set to.
The cloud init is responsible for: 
- Setting up the basics of the instance at launch
- Main thing we care about is configuring the ste clients
- These are installed prior by the 'ste_clients' role to avoid a situation where all instance launches fail due to a network/repo issue. 


Vars
------------
```
'cloud_provider'

```

Dependencies
------------
ste_clients

Author Information
------------------

Agmill3 is an elder millennial