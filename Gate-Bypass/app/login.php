<?php
// login.php
$db = new SQLite3('database.db');

$username = $_POST['username'] ?? '';
$password = $_POST['password'] ?? '';

// Requête SQL vulnérable (inchangée)
$query = "SELECT * FROM users WHERE username = '$username' AND password = '$password'";
$result = $db->query($query);

if ($result->fetchArray()) {
    // ✅ Connexion réussie : redirige vers flag.php avec un paramètre de session ou GET
    header("Location: flag.php?auth=success");
    exit();
} else {
    // ❌ Échec : redirige vers index.php avec un message d'erreur
    header("Location: index.php?error=1");
    exit();
}
?>

