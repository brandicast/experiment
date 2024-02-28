# MDADM

Check detail
<pre>
mdadm --detail /dev/md127
</pre>

<hr>

Add hdd back

<pre>
mdadm --manage /dev/md1 --re-add /dev/diskxx
</pre>

Also could try

<pre>
mdadm --manage /dev/md1 --add /dev/diskxx
</pre>
