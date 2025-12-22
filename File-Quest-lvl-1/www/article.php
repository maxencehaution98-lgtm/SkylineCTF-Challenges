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
            <?php
            if (isset($_GET['page'])) {
                $page = $_GET['page'];
                $file = "articles/" . $page . ".txt";
                
                if (file_exists($file)) {
                    echo "<div class='article-text'>";
                    include($file);
                    echo "</div>";
                } else {
                    echo "<p class='error'>❌ Article introuvable</p>";
                }
            } else {
                echo "<p class='error'>⚠️ Aucun article sélectionné</p>";
            }
            ?>
        </article>
    </main>

</body>
</html>

