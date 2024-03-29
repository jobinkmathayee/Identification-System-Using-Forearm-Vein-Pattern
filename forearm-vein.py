import cv2
import numpy as np

File_path= 'D:/GoogleDrive/2018_2019_Project/Python/Vein/database/'
Train_path= 'D:/GoogleDrive/2018_2019_Project/Python/Vein/train/'
user_name = ['a', 'b', 'c']
print ("")

for user in range (3):
    print ("Creating " + str (user_name[user]) + " skeleton")
    for i in range (5):
        image_path = File_path + user_name[user] + "/" +user_name[user] + "_" +str (i) + ".png"
##        print (image_path)
        img = cv2.imread(image_path)

##        noise
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)		// converting color image to gray image
        noise = cv2.fastNlMeansDenoising(gray)				// removing noise in image using Non-local Means Denoising algorithm 
        noise = cv2.cvtColor(noise, cv2.COLOR_GRAY2BGR)		//	noisy image is convereted again back to color image
##        print ("reduced noise")

##        equalist hist
        kernel = np.ones((7,7),np.uint8)							// creating a 7x7 matrix of 1
        img = cv2.morphologyEx(noise, cv2.MORPH_OPEN, kernel)		// It is useful in removing noise
        img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)				// converting the image to yuv
        img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])			// applying histogram equilisation to the above image
        img_output = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)		// converting back to color image
##        print ("equalized hist")

##        invert
        inv = cv2.bitwise_not(img_output)					// inverting the image white will become black and reverse
##        print ("inverted")

##        erode
        gray = cv2.cvtColor(inv, cv2.COLOR_BGR2GRAY)		// converting to gray scale
        erosion = cv2.erode(gray,kernel,iterations = 1)		// noise removal again applied
##        print ("eroded")

##        skel
        img = gray.copy()
        skel = img.copy()
        skel[:,:] = 0
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (5,5))
        iterations = 0

        while True:
            eroded = cv2.morphologyEx(img, cv2.MORPH_ERODE, kernel)
            temp = cv2.morphologyEx(eroded, cv2.MORPH_DILATE, kernel)
            temp  = cv2.subtract(img, temp)
            skel = cv2.bitwise_or(skel, temp)
            img[:,:] = eroded[:,:]
            if cv2.countNonZero(img) == 0:
                break

        print ("skeletonized")
        ret, thr = cv2.threshold(skel, 3,230, cv2.THRESH_BINARY)

        train_store = Train_path + user_name[user] + "/" +str (i+1) + ".png"
        cv2.imwrite (train_store, thr)
        print (train_store)
    print ("")
##        cv2.imshow ("", thr)
##        cv2.waitKey (0)
##        cv2.destroyAllWindows ()
