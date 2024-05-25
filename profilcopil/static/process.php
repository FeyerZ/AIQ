<?php
session_start();

if ($_SERVER["REQUEST_METHOD"] == "GET") {
    // Save the selected values in session variables
    $_SESSION['major'] = $_POST['major'];
    $_SESSION['chapter'] = $_POST['chapter'];

    // Redirect to a confirmation page or display a message
    header("Location: confirmation.html");
    exit();
}
?>
