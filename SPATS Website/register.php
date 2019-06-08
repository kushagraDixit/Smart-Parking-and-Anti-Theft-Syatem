<?php
    $er=0;
    $result="";
    $image="";
    $link=mysqli_connect("sql12.freesqldatabase.com","sql12247841","zx7wwysf1f","sql12247841");
    
    function generateRandomString($length) {
    $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    $charactersLength = strlen($characters);
    $randomString = '';
    for ($i = 0; $i < $length; $i++) {
        $randomString .= $characters[rand(0, $charactersLength - 1)];
        }
    return $randomString;
    }
    
    if(mysqli_connect_error()){
        $error ="Could Not Connect to Database!! Please Try Later!!";
    
    }else{
        if($_POST['submit']){

        if($_POST['email']!="" AND !filter_var($_POST['email'],FILTER_VALIDATE_EMAIL)){
            $error.="<br /> Please Enter a Valid Email Address!";
            $er+=1;
        }
    
        if(!$_POST['name']){
            $error.="<br /> Please Enter Your Name!";
            $er+=1;
        }

        if(!(filter_var($_POST['ph'],FILTER_VALIDATE_INT))){
            $error.="<br /> Please Enter Your Phone Number!";
            $er+=1;
        }

        if(!$_POST['pass']){
            $error.="<br /> Please Enter Your Password!";
            $er+=1;
        }
    
        if($er==0){
            $idu=generateRandomString(8);
            $un=true;
            while($un){
                $query= "SELECT * FROM spatsUsers WHERE idu='".$idu."'";
                $res=mysqli_query($link,$query);
                if($row=mysqli_fetch_array($res)){
                    $idu=generateRandomString(8);
                    $un=true;
                }else{
                    $un=false;
                }
            }
            
            $query= "INSERT INTO spatsUsers (name,e_mail,phone_no,password,idu) VALUES('".$_POST['name']."','".$_POST['email']."','".$_POST['ph']."','".$_POST['pass']."','".$idu."')";
            
            
            if($insert=mysqli_query($link,$query)){
        
            $result='<div class="alert alert-success mg"><strong>Congrats!! ' .$_POST['name']. ' You Are Registered!! Please Get a Screenshot of the QR code given Below to use SPATS</strong></div>';
            $image="<img src='https://chart.googleapis.com/chart?chs=300x300&cht=qr&chl=".$idu."'%2F&choe=UTF-8' title='".$_POST['name']."' />";
            }else{
                echo "query unsuccessfull";
            }
        }else{
            $result='<div class="alert alert-danger mg"><strong>There were error(s) in the form: </strong>'.$error.'</div';
        
        }
        }
    }

?>

<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viweport" content="width=device-width, initial-scale=1">
	<title>SMART PARKING AND ANTI THEFT SYSTEM</title>

<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">

<!-- jQuery library -->
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>

<!-- Latest compiled JavaScript -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>

<link href="https://fonts.googleapis.com/css?family=Maven+Pro:400,500,700,900" rel="stylesheet">

<style>

	#fs1 {
		font-family: 'Maven Pro', sans-serif;
	}

	.navbar-brand {

		font-size : 1.8em;
	}

	#topContainer {

		background: rgb(184, 165, 33);
		height:200px;
		width:100%;
		background-size:cover;

	}

	#topRow h1 {

		font-size:300%;
		margin-top: 200px;
	}

	#emailSignup {
		margin-top:50px;
	}

	.bold {
		font-weight: bold;
	}

	.marginTop{
		margin-top:30px;
	}

	.center{
		text-align: center;
	}

	.title{
		margin-top:100px;
		font-size:300%;
	}

	#footer{
		background-color: #B0D1FB;
		padding-top:70px;
		width:100%;
	}

	#contact{
		background-color: grey;
		padding-top:70px;
		height: 100px;
		width:100%;
	}


	.marginBottom{
		margin-bottom: 30px;
	}

	.appstoreImage{
		width:350px;
	}

	#mg{
		margin-top: 10px;
	}

	a{
		color: white;
	}

	form{
		margin: 50px auto;
	}
	
	.image{
	    text-align: center;
	}
</style>




</head>
<body data-spy="scroll" data-target=".navbar-collapse">
	<div class="navbar navbar-inverse navbar-fixed-top">
		<div class="container">
			<div class="navbar-header">
				<button class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
					<span class="icon-bar"></span>
					<span class="icon-bar"></span>
					<span class="icon-bar"></span>
				</button>
				<a class="navbar-brand" href="index.php">SPATS</a>
			</div>

			<div class="collapse navbar-collapse">
				<ul class="nav navbar-nav">
					<li class="active"><a href="index.php#topContainer">Home</a></li>
					<li><a href="index.php#details">About</a></li>
					<li><a href="index.php#footer">Download The APP</a></li>
					<li><a href="index.php#contact">Contact</a></li>
				</ul>

				<ul class="nav navbar-nav navbar-right">
					<button class="btn btn-success " id="mg"><a href="signin.php">Log IN</a></button>
					<button class="btn btn-success " id="mg"><a href="">Sign UP</a></button>
				</ul>
			</div>
		</div>
	</div>
	<div class="container contentContainer" id="fcenter">
	    

		<form method="post" >
			<h1><strong><u>REGISTER</u></strong></h1>
            <div class="form-group">
             <label for="email">Email address:</label>
             <input type="email" name="email" class="form-control" id="email" placeholder="Email" required="required">
            </div>
  
            <div class="form-group">
                <label for="name">Name</label>
                <input type="text" name="name" class="form-control" id="name" placeholder="Name" required="required">
            </div>
  
             <div class="form-group">
                <label for="phone">Phone Number</label>
                <input type="tel" name="ph" class="form-control" id="phone"  placeholder="Phone" required="required">

             </div>
            
            <div class="form-group">
                <label for="pwd">Password:</label>
                <input type="password" name="pass" class="form-control" id="pwd" placeholder="Password" required="required">
            </div>
 
            <button type="submit" class="btn btn-primary" name="submit" value="submit">Sign UP</button>
            
        </form>
        <div class="img-thumbnail image"> 
            <?php 
                echo $result;	
                
                echo $image;
                
            ?>
            </div>
            </div>
        
        
	</div>

<script>
	$(".contentContainer").css("min-height",$(window).height());


</script>	




</body>
</html>