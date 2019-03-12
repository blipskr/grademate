<?php
session_start(); //gets session id from cookies, or prepa
?>
<head>
<link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
<h1>Welcome to GradeMate!</h1>
<hr>
<table id="bar">
<tr>
  <td><a href="profile.php">My Profile</a></td>
</tr>
</table>
<hr>
<?php
if (session_id() == '' || !isset($_SESSION['login'])) { //if sid exists and login for sid exists
  
?>

<a href="login.php">Login</a>
<br>
<a href="register.php">Register</a>
<?php

} else {

  echo "You are logged in as " . $_SESSION['login'] . ".";

?>
<br>
<a href="logout.php">Logout</a>

<?php 

}
?>
</body>
