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
            if (!isset($_GET['page']) || empty($_GET['page'])) {
                echo "<p class='error'>❌ Aucun article spécifié</p>";
                exit;
            }

            $page = $_GET['page'];

            // 🛡️ FILTRE : Retire les ..../ et ....\ avant de vérifier
            $cleaned = str_replace(['..../', '....\\'], ['', ''], $page);

            // Vérifie s'il reste des ../ ou ..\
            if (strpos($cleaned, '../') !== false || strpos($cleaned, '..\\') !== false) {
                echo "<p class='error'>🚫 Caractères non autorisés détectés !</p>";
                exit;
            }

            // Construction du chemin (avec le répertoire articles/)
            $filepath = "articles/" . $page . ".txt";

            // 🔧 NORMALISATION MANUELLE : Convertit ....// en ../
            $filepath = str_replace('..../', '../', $filepath);
            $filepath = str_replace('....\\', '..\\', $filepath);

            // Lecture du fichier
            if (file_exists($filepath)) {
                $content = file_get_contents($filepath);
                echo "<div class='article-text'>" . nl2br(htmlspecialchars($content)) . "</div>";
            } else {
                echo "<p class='error'>❌ Article introuvable</p>";
            }
            ?>
        </article>
    </main>

    <footer>
        <div class="container">
            <p>&copy; 2024 ESGI Tech Blog - Tous droits réservés</p>
        </div>
    </footer>
</body>
</html>
