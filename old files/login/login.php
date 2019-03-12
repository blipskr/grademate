<?php
session_start(); //gets session id from cookies, or prepa
?>
<head>
<link rel="stylesheet" type="text/css" href="style.css">
</head>
<?php
require_once('config.inc.php');
$con = new mysqli($database_host, $database_user, $database_pass, $group_dbnames[0]);

if (isset($_POST['login']) && isset($_POST['password'])) //when form submitted
{
  $username = $_POST["login"];
  $password = $_POST["password"];
  $queryName = "SELECT Username FROM Login WHERE Username='$username' AND Password='$password'";
  $resultName = $con->query($queryName);

  if ($resultName->num_rows != 0)
  {
    $_SESSION['login'] = $_POST['login']; //write login to server storage
?>
<script type="text/javascript">
window.location.href = 'index.php';
</script>
<?php
  }
  else
  {
    echo "<script>alert('Wrong login or password');</script>";
    echo "<noscript>Wrong login or password</noscript>";
  }
}
$con -> close();
?>
<h1>Login Now!</h1>
<hr>
<form method="post">
  Login:<br><input name="login"><br>
  Password:<br><input name="password" type="password"></input><br>
  <input type="submit">
</form>
<br>
<a href="register.php">Register</a>
