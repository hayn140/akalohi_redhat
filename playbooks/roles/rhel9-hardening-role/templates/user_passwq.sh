#!/bin/bash
for user in $(awk -F: '{if ($3 >= 1000 && $1 != "nobody") print $1 }' /etc/passwd); do
      chage --maxdays 60 $user
done

