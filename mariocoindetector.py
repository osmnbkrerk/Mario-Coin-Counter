import cv2
import numpy as np
import math


def listedeDegil(yeniNesne):
    for tespitEdilmisObje in tespitEdilmisObjeler:
        if math.hypot(yeniNesne[0] - tespitEdilmisObje[0], yeniNesne[1] - tespitEdilmisObje[1]) < thresholdDist:
            return False
    return True


img = cv2.imread("resimler/mario2.jpg")
griResim = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
sablon = cv2.imread("resimler/mario_coin.jpg", 0)
w, h = sablon.shape[::-1]

maske = cv2.adaptiveThreshold(sablon,255,cv2.CALIB_CB_ADAPTIVE_THRESH, cv2.THRESH_BINARY,33,2) #maskeyi kendim paintten cizmeyi deneyince matchTemplate fonk.ta hata alıyorum
sonuc = cv2.matchTemplate(griResim, sablon, cv2.TM_CCORR_NORMED, None, maske) #sablon eslestirmeyi yapiyoruz
threshold = 0.997 #threshold degerini deneme yanilma yoluyla verdim

loc = np.where(sonuc >= threshold)
tespitEdilmisObjeler = []
thresholdDist = 30

for pt in zip(*loc[::-1]):
    if len(tespitEdilmisObjeler) == 0 or listedeDegil(pt):
        tespitEdilmisObjeler.append(pt)
    cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (255, 190, 10), 2)


cv2.putText(img,"Altin Sayisi = " + str(len(tespitEdilmisObjeler)),(10,100), cv2.FONT_HERSHEY_COMPLEX, 1,(255,255,255),2)

cv2.imshow("Mario", img)
print("Bulunan altın sayısı = ", len(tespitEdilmisObjeler))
k = cv2.waitKey(0)
if k == 27:
    cv2.destroyAllWindows()
elif k == ord('s'):  # s'ye basarak resmi, 'resimler' klasörünün altına kaydedebilirsiniz
    cv2.imwrite('resimler/sonHali.jpg',img)
    print("....Resim kaydedildi....")
cv2.waitKey(0)
