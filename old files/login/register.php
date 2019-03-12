<style><?php include 'style.css'; ?></style>
<?php
require_once('config.inc.php');
$con = new mysqli($database_host, $database_user, $database_pass, $group_dbnames[0]);

//TODO: do not hardcode, get from database

if (isset($_POST['login']) && isset($_POST['password'])) //when form submitted
{
  $username = $_POST["login"];
  $password = $_POST["password"];
  $queryName = "SELECT Username FROM Login WHERE Username='$username'";
  $resultName = $con->query($queryName);
  if ($resultName->num_rows == 0)
  {
    $sql = "INSERT INTO Login (Username, Password) VALUES ('$username', '$password')";
    mysqli_query($con, $sql);
?>
<script type="text/javascript">
window.location.href = 'index.php';
</script>
<?php
  }
  else
  {
    echo "<script>alert('You are already registered!');</script>";
    echo "<noscript>You are already registered!</noscript>";
  }
}

?>
<h1>Register Now!</h1>
<hr>
<form method="post">
  Username:<br><input name="login"><br>
  Password:<br><input name="password" type="password"><br>
  <input type="submit">
</form>
<br>
<a href="login.php">Login</a>
