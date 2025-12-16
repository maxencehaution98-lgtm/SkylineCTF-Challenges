# Gate Bypass

## SQL Injection
En nous rendant sur l'URL donné par le chall nous pouvons voir une page assez simple, une page de login. Cette page est faillible aux Injection SQL, nous pourrons donc Bypass l'authentifiacation grâce à une injection simple.

Voici un exemple :
l'utilisateur qui nous intéresse dans ce cas de figure est ``admin``, nous pouvons commencer à rentrer cet utilisateur : 
username : admin
password : ??

Maintenant vu que nous ne connaissons pas le mot de passe nous allons l'échapper grâce aux caractères suivants : ``' --``
Ces caractères vont commenter le reste de la ligne, donc pas de vérification de mot de passe. 

Voici l'Injection SQL complète :
````
username : admin' --
password : kakoukakou
````

le mot de passe n'est pas le bon mais on s'en fiche qu'il n'est pas vérifié. Nous sommes obligé de mettre un mot de passe car le champs ne doit pas être vide.

Une fois authentifié, nous pouvons voir le flag : 
```
SKL{SQLi-1nJ3cT1oN}
```