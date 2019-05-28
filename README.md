# RetinopathyDetection
In this repo you will get all required files details description is avaiable in report.
list of uploaded files

#1. 80-20Standarded.csv
This is dataset file which was created by us. We have used around 1192 images to genrate this csv file.
consist 13 column:- NAME	MA	ENTRGB	ENTMA	ENGGREE	ENGBV	HOMO	EX	ENTBV	ENGMA	CONTRA	BR	BI	LABEL
MA:- microaneurusms ENTRGB:- Entropy RGB image ENTMA:- Entropy microaneurusms ENGGREE:- Energy Green Channel
ENGBV:- Energy BloodVessel HOMO:- Homogenity EX:- Exedute ENTBV:- Entropy Blood Vessel ENGMA:- Energy microaneurusms
CONTRA:- contrast BR:- Blood Vessel real part BI:- Blood Vessel Imagenery Label
This terms are explain in report.

#2. DRD.py
It is file which extact feature from RGB image and pass it to model and genrate result.
each feature mentioned in dataset is extracted from input image. In order to create your own dataset file for your own dataset you can use this code and create your dataset.

#3. RetinopathyDetectionReport.pdf
Total work report is in this PDF.
 
#4. SVM.sav
Our saved model.

#5.ui.html
simple html file provide gui to upload image in order to get result.
and avoid hide inner implementation and complexity.

#6. upload.php
php code which allow to upload image and run python script in localhost



