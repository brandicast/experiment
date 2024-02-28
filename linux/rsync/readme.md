# rsync

To rsync remote smb folder

<pre>

rsync -av -e 'ssh -p $PORT'  $LOCAL_FOLDER $USERNAME@$REMOTE_IP:$REMOTE_FOLDER

</pre>


parameters:

z for compression


<hr>

To login without password:

<pre>
 sshpass -p "password" rsync root@1.2.3.4:/abc /def
 </pre>

> Note the space at the start of the command, in the bash shell this will stop the command (and the password) from being stored in the history. I don't recommend using  he RSYNC_PASSWORD variable unless absolutely necessary (as per a previous edit to this answer), I recommend suppressing history storage or at least clearing history after. In addition, you can use tput reset to clear your terminal history.