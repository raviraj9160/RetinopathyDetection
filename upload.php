<!DOCTYPE html>
<head>
<title>RESULT</title>
<style>
.container
{
margin-top:20px;
margin-left:20px;

font-size: 30px;
}
body {
 background-color: #cccccc;
}
h1, h2
{
margin-top:20px;
margin-left:20px;
}
</style>
</head>

<body>
<h1 style="color: red;">DIAGNOSIS RESULT</h1>
<div class="container">

</div>
</body>
</html>
<?php
$target_dir = "uploads/";
$target_file = $target_dir.basename($_FILES["fileToUpload"]["name"]);
$uploadOk = 1;
$imageFileType = strtolower(pathinfo($target_file,PATHINFO_EXTENSION));
// Check if image file is a actual image or fake image
if(isset($_POST["submit"])) {
    $check = getimagesize($_FILES["fileToUpload"]["tmp_name"]);
    if($check !== false) {
        //echo "File is an image - " . $check["mime"] . ".";
        $uploadOk = 1;
    } else {
        echo "File is not an image.";
        $uploadOk = 0;
    }
}
// Check if file already exists
if (file_exists($target_file)) {
    echo "Sorry, file already exists.";
    $uploadOk = 0;
}
// Check file size

// Allow certain file formats
if($imageFileType != "jpg" && $imageFileType != "png" && $imageFileType != "jpeg"
&& $imageFileType != "gif" ) {
    echo "Sorry, only JPG, JPEG, PNG & GIF files are allowed.";
    $uploadOk = 0;
}
// Check if $uploadOk is set to 0 by an error
if ($uploadOk == 0) {
    echo "Sorry, your file was not uploaded.";
// if everything is ok, try to upload file
} else {
    if (move_uploaded_file($_FILES["fileToUpload"]["tmp_name"], $target_file)) {
        //echo "The file ". basename( $_FILES["fileToUpload"]["name"]). " has been uploaded.";
    } else {
        echo "Sorry, there was an error uploading your file.";
    }
}
$ch="chmod 777 /var/www/html/DRDFinal/uploads/".basename($_FILES["fileToUpload"]["name"]);
shell_exec($ch);


$descriptorspec = array(
   0 => array("pipe", "r"),  // stdin is a pipe that the child will read from
   1 => array("pipe", "w"),  // stdout is a pipe that the child will write to
   2 => array("file", "./error-output.txt", "a") // stderr is a file to write to
);
$process = proc_open('/home/raviraj/PycharmProjects/Diabetic/venv/bin/python DRD.py', $descriptorspec, $pipes);

if (is_resource($process)) {
    // $pipes now looks like this:
    // 0 => writeable handle connected to child stdin
    // 1 => readable handle connected to child stdout
    // Any error output will be appended to /tmp/error-output.txt

    fwrite($pipes[0], $target_file);
    fclose($pipes[0]);

    $ch1="chmod 777 /var/www/html/DRDFinal/uploads/BloodVessel.png";
   shell_exec($ch1);
   $ch2="chmod 777 /var/www/html/DRDFinal/uploads/MA.png";
   shell_exec($ch2);
   $ch3="chmod 777 /var/www/html/DRDFinal/uploads/exudates.png";
   shell_exec($ch3);

    //echo '<div align="center"><h1>'.stream_get_contents($pipes[1]).'</h1></div>';
    echo '<h2>'.stream_get_contents($pipes[1]).'</h2>';
    fclose($pipes[1]);

    $error=file_get_contents("error-output.txt");
            echo $error;

    // It is important that you close any pipes before calling
    // proc_close in order to avoid a deadlock
    $return_value = proc_close($process);

   exec("rm error-output.txt");

}
$rm="rm /var/www/html/DRDFinal/uploads/".basename($_FILES["fileToUpload"]["name"]);
shell_exec($rm);

?>
