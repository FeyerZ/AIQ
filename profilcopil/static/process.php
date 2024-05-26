<?php
session_start();

if ($_SERVER["REQUEST_METHOD"] == "GET") {
    // Save the selected values in session variables
    $_SESSION['domain'] = $_POST['domain'];
    $_SESSION['subdomain'] = $_POST['subdomain'];

    // Redirect to a confirmation page or display a message
    header("Location: confirmation.html");
    exit();
}
?>
