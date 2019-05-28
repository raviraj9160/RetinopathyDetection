import cv2
import numpy as np
import pickle
import skimage
from skimage import feature, io
from sklearn import preprocessing
from pywt import dwt2
import warnings
warnings.filterwarnings("ignore")

maxMA=  329
maxENTRGB=  7.418652205800001
maxENTMA=  0.1024361719
maxENGGREE=  134.35548114780002
maxENGBV=  6892.646527290401
maxHOMO=  0.9642819367000001
maxEX=  4585
maxENTBV=  0.7703997579999999
maxENGMA=  223.6797094345
maxCONTRA=  3.5897680287

featureVector=[]
path=input()
img = cv2.imread(path)


img = cv2.resize(img,(512,512),interpolation=cv2.INTER_CUBIC)
b,g,r = cv2.split(img)

#ENTROPY

ENTRGB = skimage.measure.shannon_entropy(img)
ENTRGB=ENTRGB/maxENTRGB

clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
claheImg = clahe.apply(g)
edge = cv2.Canny(claheImg, 160, 15)
ENTBV = skimage.measure.shannon_entropy(edge)
ENTBV=ENTBV/maxENTBV

kernel = np.ones((2, 2), np.uint8)
erosion = cv2.erode(edge, kernel, iterations=1)
dilation = cv2.dilate(erosion, kernel, iterations=2)
opening = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, kernel)
ENTMA = skimage.measure.shannon_entropy(opening)
ENTMA=ENTMA/maxENTMA


#ENERGY

clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
claheImg = clahe.apply(g)

claheImg = claheImg.T
_, (cH, cV, cD) = dwt2(claheImg, 'db1')
ENGGREE = (cH ** 2 + cV ** 2 + cD ** 2).sum() / claheImg.size
ENGGREE=ENGGREE/maxENGGREE

edge = cv2.Canny(claheImg, 160, 15)
#cv2.imwrite('/var/www/html/DRDFinal/uploads/BloodVessel.png',edge)
edge = edge.T
_, (cH, cV, cD) = dwt2(edge, 'db1')
ENGBV = (cH ** 2 + cV ** 2 + cD ** 2).sum() / edge.size
ENGBV=ENGBV/maxENGBV

kernel = np.ones((2, 2), np.uint8)
erosion = cv2.erode(edge, kernel, iterations=1)
dilation = cv2.dilate(erosion, kernel, iterations=2)
opening = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, kernel)
opening = opening.T
_, (cH, cV, cD) = dwt2(opening, 'db1')
ENGMA = (cH ** 2 + cV ** 2 + cD ** 2).sum() / opening.size
ENGMA=ENGMA/maxENGMA



#HOMO AND CONTRAST
b, img, r = cv2.split(img)
S = preprocessing.MinMaxScaler((0, 11)).fit_transform(img).astype(int)
Grauwertmatrix = feature.greycomatrix(S, [1, 2, 3], [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4], levels=12,
                                      symmetric=False, normed=True)

ContrastStats = feature.greycoprops(Grauwertmatrix, 'contrast')
HomogeneityStats = feature.greycoprops(Grauwertmatrix, 'homogeneity')

CONTRA=np.mean(ContrastStats)
CONTRA=CONTRA/maxCONTRA
HOMO=np.mean(HomogeneityStats)
HOMO=HOMO/maxHOMO

#MA

clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
claheImg = clahe.apply(g)
edge = cv2.Canny(claheImg, 160, 15)
kernel = np.ones((2, 2), np.uint8)
erosion = cv2.erode(edge, kernel, iterations=1)
dilation = cv2.dilate(erosion, kernel, iterations=2)
opening = cv2.morphologyEx(dilation, cv2.MORPH_OPEN, kernel)
#cv2.imwrite('/var/www/html/DRDFinal/uploads/MA.png',opening)
cnts = cv2.findContours(opening, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]
s1 = 1
s2 = 100
xcnts = []
for cnt in cnts:
    if s1 < cv2.contourArea(cnt) < s2:
        xcnts.append(cnt)
MA=len(xcnts)
MA=MA/maxMA

#exudates

clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
claheImg4 = clahe.apply(g)

edge = cv2.Canny(claheImg4, 160, 15)

kernel = np.ones((2, 2), np.uint8)
strEl = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

erosion = cv2.erode(edge, kernel, iterations=1)
dilation = cv2.dilate(erosion, strEl, iterations=2)
closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, strEl)
#cv2.imwrite('/var/www/html/DRDFinal/uploads/exudates.png',closing)

n_white_pix = np.sum(closing == 255)

EX=n_white_pix
EX=EX/maxEX

#appending to feature vector
featureVector.append(MA)
featureVector.append(ENTRGB)
featureVector.append(ENTMA)
featureVector.append(ENGGREE)
featureVector.append(ENGBV)
featureVector.append(HOMO)
featureVector.append(EX)
featureVector.append(ENTBV)
featureVector.append(ENGMA)
featureVector.append(CONTRA)

#acutual working
dc=np.array(featureVector)
dc=dc[:,np.newaxis]
dc=dc.reshape(1,10)
#print("feature vector ",dc)

RF_model="/var/www/html/DRDFinal/SVM.sav"
load_rf=pickle.load(open(RF_model, 'rb'))
pred=load_rf.predict(dc)

if pred==1:
    print("This patient is affected with Retinopathy ")
else:
    print("This patient is not affected with Retinopathy ")
