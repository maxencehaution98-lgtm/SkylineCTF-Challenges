<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ESGI - Flag Capturé</title>
    <link rel="stylesheet" href="style.css">
    <link rel="stylesheet" href="flag.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body>
    <?php
    // Vérifie si l'utilisateur est authentifié
    if (!isset($_GET['auth']) || $_GET['auth'] !== 'success') {
        header("Location: index.php?error=unauthorized");
        exit();
    }
    ?>

    <div class="flag-container">
        <div class="logo">ESGI</div>
        <h1>Accès Administrateur Autorisé</h1>

        <div class="success-icon">
            <i class="fas fa-check-circle"></i>
        </div>

        <div class="flag-title">
            Félicitations ! Voici votre flag :
        </div>

        <div class="flag">
            SKL{SQLi-1nJ3cT1oN}
        </div>
	    </br>
        <a href="index.php" class="btn-back">
            <i class="fas fa-arrow-left"></i> Retour à la connexion
        </a>

    </div>
</body>
</html>

