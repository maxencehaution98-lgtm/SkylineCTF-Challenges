<!DOCTYPE html>
<html>
<head>
    <title>Login Bypass Challenge - ESGI</title>
    <link rel="stylesheet" href="style.css">
    <link rel="icon" href="favicon.ico" type="image/x-icon">
</head>
<body>
    <div class="login-container">
        <div class="logo">ESGI</div>
        <h1>Connexion Admin</h1>

        <!-- Affichage des erreurs -->
        <?php
        if (isset($_GET['error'])) {
            $error = $_GET['error'];
            if ($error == '1') {
                echo '<div class="error-message">Identifiants incorrects.</div>';
            } elseif ($error == 'unauthorized') {
                echo '<div class="error-message">Accès non autorisé. Veuillez vous connecter.</div>';
            }
        }
        ?>

        <form action="login.php" method="POST">
            <div class="form-group">
                <label for="username">Utilisateur :</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div class="form-group">
                <label for="password">Mot de passe :</label>
                <input type="password" id="password" name="password" required>
            </div>
            <button type="submit" class="btn-login">Se connecter</button>
        </form>

    </div>
</body>
</html>

