<html dir="[direction]" lang="[language]" class="[class names]">
	<head>
    /* Import all the necessary bits */
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
 <link rel="stylesheet" href="https://code.getmdl.io/1.3.0/material.light_blue-deep_purple.min.css" />
     <script defer src="https://code.getmdl.io/1.3.0/material.min.js"></script>
       <link rel="stylesheet" type="text/css" href="css/dialog-polyfill.css" />
			        <link rel="stylesheet" type="text/css" href="css/test.css" />
       <link rel="stylesheet" href="http://fonts.googleapis.com/css?family=Roboto:300,400,500,700" type="text/css">

		<title>Grademate</title>
	</head>
    <!-- Always shows a header, even in smaller screens. -->
<!--____________________________Navigation Bar______________________________ -->

<div class="mdl-layout mdl-js-layout mdl-layout--fixed-header">
  <header class="mdl-layout__header">
    <div class="mdl-layout__header-row">
      <!-- Title -->
      <span class="mdl-layout-title"><img src="images/grademate.png"  height="38" width="196" href="index.html"></span>
      <!-- Add spacer, to align navigation to the right -->
      <div class="mdl-layout-spacer"></div>
      <!-- Navigation. We hide it in small screens. -->
      <nav class="mdl-navigation mdl-layout--large-screen-only">
      <button class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent">
        About
      </button>
      <br>
      <button class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent">
        Contact
      </button>
      <button class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent">
        Agreement/User Policy
      </button>
			<button class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent"
      onclick="location.href='login.php'">
        Login
      </button>
			<button class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent"
			onclick="location.href='register.php'">
				Register
			</button>

      <!-- show the dialog for the clicks -->
      <body>
    <button id="show-dialog" type="button" class="mdl-button">About</button>
  <dialog class="mdl-dialog">
    <h4 class="mdl-dialog__title">About</h4>
    <div class="mdl-dialog__content">
      <p>
      Grademate is about having fun, and is made with love. ( ͡° ͜ʖ ͡°)
      <br>Authors:
       <ul>
  <li>Brian</li>
  <li>Josh</li>
  <li>Ilia</li>
    <li>Robert</li>
      <li>Andy</li>
        <li>Danielius</li>
          <li>Stephen</li>
            <li>Kamil</li>
          </ul>
      </p>
    </div>
    <div class="mdl-dialog__actions">
      <button type="button" class="mdl-button close">Cool</button>
    </div>
  </dialog>
    <script src="javascript/dialog-polyfill.js"></script>
  <script>
    var dialog = document.querySelector('dialog');
    var showDialogButton = document.querySelector('#show-dialog');
    if (! dialog.showModal) {
      dialogPolyfill.registerDialog(dialog);
    }
    showDialogButton.addEventListener('click', function() {
      dialog.showModal();
    });
    dialog.querySelector('.close').addEventListener('click', function() {
      dialog.close();
    });
  </script>

      </nav>
    </div>
  </header>
  <div class="mdl-layout__drawer">
    <span class="mdl-layout-title">Title</span>
    <nav class="mdl-navigation">
  </div>

</div>
<!--_____________________________ banner section   _________________________ -->
    <!--
    Styling for the banner
  -->
    <style type="text/css">
#banner {
    background-image: url('images/background.jpg');
    background-size: cover;
    background-repeat: no-repeat;
    height: 50%;
    width: 100%;
    margin: 0 auto;
    text-align: center;
    color: white;
    background-color: lightblue;
    display: flex;
    justify-content: center; /* align horizontal */
    align-items: center; /* align vertical */
    bagfilter: blur(5px);
}
</style>
    <div class="mdl-grid">
  <div class="mdl-cell mdl-cell--1-col" id="banner">
<div class="bgimg">
<h1 style=font-size:200px>Grademate</h1>
<h3>Improve your grades with your mates<h3>
</div>
  </div>
</div>

<!--- ErrorMessage for already registered user --->
<dialog class="mdl-dialog" id="errormessage">
	<h4 class="mdl-dialog__title">Error!</h4>
	<div class="mdl-dialog__content">
<p>Username and/or password incorrect. Please try again.</p>
	</div>
	<div class="mdl-dialog__actions">
		<button type="button" class="mdl-button close">Cool</button>
	</div>
</dialog>
	<script src="javascript/dialog-polyfill.js"></script>
<script>
	var error = document.querySelector('#errormessage');
	var showErrorButton = document.querySelector('#submit');
	if (! error.showModal) {
		dialogPolyfill.registerDialog(error);
	}
	error.querySelector('.close').addEventListener('click', function() {
		error.close();
	});
</script>

<!--- Register PHP --->
<div class="mdl-layout mdl-js-layout"
<main class="mdl-layout__content">
	<div class="page-content">
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
		window.location.href = 'index.html';
		</script>
		<?php
		  }
		  else
		  {
				?> <script>error.showModal()</script> <?php
		  }
		}
		$con -> close();
		?>
		<style>
    .mdl-grid.center-items {
      justify-content: center;
    }
</style>

<!--- Register Form --->
<div class="mdl-grid center-items">

			<form method="post">

				<div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
					<input class="mdl-textfield__input" type="text" name="login">
					<label class="mdl-textfield__label">Username:</label>
				</div>
				<br>
				<div class="mdl-textfield mdl-js-textfield mdl-textfield--floating-label">
					<input class="mdl-textfield__input" type="password" name="password">
					<label class="mdl-textfield__label">Password:</label>
				</div>
				<br>
				<button class="mdl-button mdl-js-button mdl-button--raised mdl-button--accent" type="submit" id="submit">
					Submit
				</button>
			</form>
			<br>
		</div>
		</div>
		</div>



</main>
</div>
<!-- _________________________________ footer section________________________-->
	</body>
</html>
