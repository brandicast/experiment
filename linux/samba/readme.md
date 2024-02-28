# SAMBA

configuration file :


/etc/samba/smb.conf

<br>

<pre>
workgroup = myworkgroup

if add new share

[myshare]
   comment = Brandon's Share
   path = /home/hhwu
   valid users = hhwu
   public = no
   writable = yes
   printable = no
   create mask = 0765

</pre>

<br>
To add new user:

<br>

<pre>
	smbpassword -a username
</pre>

 and enter password.


*note*

如果一切都設好之後，但是從windows上看的到分享卻無法進入，則可試著改變SELinux的設定。