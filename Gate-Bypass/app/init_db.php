<?php
// Création de la base de données SQLite et de l'utilisateur admin
$db = new SQLite3('database.db');
$db->exec("CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
)");
// Ajout de l'utilisateur admin (mot de passe arbitraire, non utilisé grâce à la SQLi)
$db->exec("INSERT INTO users (username, password) VALUES ('admin', '%F8l7YTMC7xjC7&J$wDc^1')");
echo "Base de données initialisée avec l'utilisateur 'admin'.";
?>

