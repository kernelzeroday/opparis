#!/usr/bin/python

import numpy as np
import cv2
import copy
import os
import sys

"""
DEPENDANCIES

python 2.7
opencv2.4.9 (might work with other versions - not 3.*)

If you have trouble getting this working, try installing non-free features of opencv

To install opencv non-free
	sudo add-apt-repository --yes ppa:xqms/opencv-nonfree
	sudo apt-get update 
	sudo apt-get install libopencv-nonfree-dev


ALSO REQUIRED
stock image of ISIS flag in the current path named 'flag.png'
	https://www.anony.ws/image/JbwP

center of ISIS flag in current path named 'circle.png'
	https://www.anony.ws/image/JbwH


This algo works by extracting shapes from the original image and comparing it to shapes extracted from a stock ISIS flag image.
The more shapes that match, the more likely the original image contains an ISIS flag.
"""



#NOTE this function was taken from a post on stackexchange 
def drawMatches(img1, kp1, img2, kp2, matches):
    """
    My own implementation of cv2.drawMatches as OpenCV 2.4.9
    does not have this function available but it's supported in
    OpenCV 3.0.0

    This function takes in two images with their associated 
    keypoints, as well as a list of DMatch data structure (matches) 
    that contains which keypoints matched in which images.

    An image will be produced where a montage is shown with
    the first image followed by the second image beside it.

    Keypoints are delineated with circles, while lines are connected
    between matching keypoints.

    img1,img2 - Grayscale images
    kp1,kp2 - Detected list of keypoints through any of the OpenCV keypoint 
              detection algorithms
    matches - A list of matches of corresponding keypoints through any
              OpenCV keypoint matching algorithm
    """

    # Create a new output image that concatenates the two images together
    # (a.k.a) a montage
    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1]

    out = np.zeros((max([rows1,rows2]),cols1+cols2,3), dtype='uint8')

    # Place the first image to the left
    out[:rows1,:cols1] = np.dstack([img1, img1, img1])

    # Place the next image to the right of it
    out[:rows2,cols1:] = np.dstack([img2, img2, img2])

    # For each pair of points we have between both images
    # draw circles, then connect a line between them
    for mat in matches:

        # Get the matching keypoints for each of the images
        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx

        # x - columns
        # y - rows
        (x1,y1) = kp1[img1_idx].pt
        (x2,y2) = kp2[img2_idx].pt

        # Draw a small circle at both co-ordinates
        # radius 4
        # colour blue
        # thickness = 1
        cv2.circle(out, (int(x1),int(y1)), 4, (255, 0, 0), 1)   
        cv2.circle(out, (int(x2)+cols1,int(y2)), 4, (255, 0, 0), 1)

        # Draw a line in between the two points
        # thickness = 1
        # colour blue
        cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), (255, 0, 0), 1)


    # Show the image

    # Also return the image if you'd like a copy
    return out


def rotate(image, angle, center = None, scale = 1.0):
	"""
		Rotates a cv2 image. This function has been ripped off someone on stackexchange.
	"""
	(h, w) = image.shape[:2]

	if center is None:
		center = (w / 2, h / 2)

	# Perform the rotation
	M = cv2.getRotationMatrix2D(center, angle, scale)
	rotated = cv2.warpAffine(image, M, (w, h))
	return rotated



def detect_flag_method1(filename):
	#load image as a grayscale
	raw_img = cv2.imread(filename)
	raw_img = cv2.resize(raw_img, (1920, 1080))

	img2 = cv2.imread(filename, 0)

	#create a folder to store potential matches in 
	folder = "matches"
	if not os.path.exists(folder):
		os.makedirs(folder)

	for the_file in os.listdir(folder):
		file_path = os.path.join(folder, the_file)
		try:
		    if os.path.isfile(file_path):
		        os.unlink(file_path)
		except Exception, e:
		    print e

	#resize image. this seems to help with getting consistent results
	img2 = cv2.resize(img2, (1920, 1080))

	#adding some gaussian blur helps remove artifacts once threshold is applied
	blur = cv2.GaussianBlur(img2,(11,11),0)
	#because the flag is black and white, it's easy to pick it out by applying a threshold
	ret3,image_thresh = cv2.threshold(img2, 140,255, 0)
	#save a copy of threshold image for human inspection
	cv2.imwrite('img_threshold.png', image_thresh)

	img_contours = copy.deepcopy(image_thresh)
	#find the contours - basically edge detection
	img_contours, hierarchy = cv2.findContours(img_contours, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	#load the stock flag image, apply threshold and contours for that too
	img1 = cv2.imread('circle.png',0)
	ret, thresh = cv2.threshold(img1,127,255,0)
	flag_contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	f_contours = copy.deepcopy(img1)
	f_contours[:] = (0)
	cv2.drawContours(f_contours, flag_contours, -1, 255,2)
	cv2.imwrite('flag_contours.png', f_contours)

	#save a copy of image contours so we can see what opencv  sees
	timg = copy.deepcopy(img2)
	timg[:] = (0)
	cv2.drawContours(timg, img_contours, -1, 255,1)
	cv2.imwrite('img_contours.png', timg)


	#first we'll try and find the big circle, because that's the easiest part to detect
	#actually, this function is way too slow so it's commented out for now
	circle_img = cv2.imread('circle.png',0)

	#create a list to store interesting parts of the image
	img_bits = []

	#iterate through image contours
	count = 0
	for ic in img_contours:
		#deep copy image2 - same as making new image but maybe a bit faster?
		timg = copy.deepcopy(img2)
		#set all to zero
		timg[:] = (0)
	
		#draw contours onto tempory image
		cv2.drawContours(timg, [ic], 0, 255, 1)
	
		#now do an 'autocrop' to leave only the interesting part of the image
		x,y,w,h = cv2.boundingRect(ic)
		#ignore parts that are too small
		if(w < 30) or (h < 30):
			continue

		crop = image_thresh[y:y+h,x:x+w]
		#resize everything to 100x100
		img_piece = cv2.resize(crop, (100, 100))
		cv2.imwrite("matches/piece"+str(count)+".png", img_piece)
		count += 1
	
		crop = img2[y:y+h,x:x+w]
		#resize everything to 100x100
		img_piece2 = cv2.resize(crop, (100, 100))
		img_bits.append((img_piece, img_piece2))


	match_score = 0
	count = 0
	fc_count = 0
	flag_found = False
	for fc in flag_contours:
		fc_count += 1
		timg = copy.deepcopy(img1)
		timg[:] = (0)
	
		cv2.drawContours(timg, [fc], 0, 255, 1)
	
		#now do an 'autocrop'
		x,y,w,h = cv2.boundingRect(fc)
		#ignore parts that are too small
		if(w < 60) or (h < 60):
			continue
		crop = img1[y:y+h,x:x+w]
		flag_piece = cv2.resize(crop, (100, 100))
	
		ic_count = 0
		for ic in img_bits:
		
			sift = cv2.ORB()

			# find the keypoints and descriptors with SIFT
			kp1, des1 = sift.detectAndCompute(ic[0],None)
			kp2, des2 = sift.detectAndCompute(flag_piece,None)

			# create BFMatcher object
			bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

			# Match descriptors.
			matches = bf.match(des1,des2)

			# Sort them in the order of their distance.
			matches = sorted(matches, key = lambda x:x.distance)

			if(len(matches) < MIN_MATCH_COUNT):
				#print "Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT)
				matchesMask = None
				continue
			flag_piece = cv2.resize(crop, (100, 100))
			img3 = drawMatches(ic[1],kp1,flag_piece,kp2,matches)
			cv2.imwrite("matches/match"+str(count)+"_.png", img3)
			cv2.imwrite("matches/match"+str(count)+"_color.png", ic[0])
		
			rot = 0
			while(rot < 360):
				template = rotate(flag_piece, rot)
				result = cv2.matchTemplate(ic[0], template, cv2.TM_SQDIFF_NORMED)
			
				#if(matchy_ness < 0):
				#	matchy_ness = -matchy_ness
			
				if(result < 0.6):
					cv2.imwrite('matches/match' + str(count) + '_pattern.png', ic[1])
					cv2.imwrite("matches/match"+str(count)+"_color.png", ic[0])
					cv2.imwrite("matches/match"+str(count)+"_flag.png", template)
					count += 1
				
					msg = str(count) + " " + str(result)
					print msg
					flag_found = True
					break
			
				rot += 10
			ic_count += 1
	return flag_found


def detect_flag_method2(filename):
	#this is mostly the same as the previous function, except we compare pieces of the whole flag, rather than just looking for the circle

	folder = "matches"
	if not os.path.exists(folder):
		os.makedirs(folder)

	for the_file in os.listdir(folder):
		file_path = os.path.join(folder, the_file)
		try:
		    if os.path.isfile(file_path):
		        os.unlink(file_path)
		except Exception, e:
		    print e

	raw_img = cv2.imread(filename)
	raw_img = cv2.resize(raw_img, (1920, 1080))

	img2 = cv2.imread(filename, 0)

	img2 = cv2.resize(img2, (1920, 1080))
	blur = cv2.GaussianBlur(img2,(11,11),0)
	ret3,image_thresh = cv2.threshold(img2, 80,255, 0)
	img_contours = copy.deepcopy(image_thresh)
	img_contours, hierarchy = cv2.findContours(img_contours, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	img1 = cv2.imread('flag.png',0)
	ret, thresh = cv2.threshold(img1,100,255,0)
	flag_contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	f_contours = copy.deepcopy(img1)
	f_contours[:] = (0)
	cv2.drawContours(f_contours, flag_contours, -1, 255,2)
	timg = copy.deepcopy(img2)
	timg[:] = (0)
	cv2.drawContours(timg, img_contours, -1, 255,1)
	img_bits = []

	count = 0
	for ic in img_contours:
		timg = copy.deepcopy(img2)
		timg[:] = (0)
		cv2.drawContours(timg, [ic], 0, 255, 1)
		x,y,w,h = cv2.boundingRect(ic)
		if(w < 50) or (h < 50):
			continue
		if(w > 500) or (h > 400):
			continue
		crop = image_thresh[y:y+h,x:x+w]
		img_piece = cv2.resize(crop, (100, 100))
		count += 1
		crop = img2[y:y+h,x:x+w]
		img_piece2 = cv2.resize(crop, (100, 100))
		cv2.imwrite('matches/piece' + str(count) + '.png', img_piece)
		count += 1
		img_bits.append((img_piece, img_piece2))


	match_score = 0
	count = 0
	fc_count = 0
	for fc in flag_contours:
		timg = copy.deepcopy(img1)
		timg[:] = (0)
	
		cv2.drawContours(timg, [fc], 0, 255, 1)
	
		x,y,w,h = cv2.boundingRect(fc)
		if(w < 40) or (h < 40):
			continue
		crop = img1[y:y+h,x:x+w]
		flag_piece = cv2.resize(crop, (100, 100))
		cv2.imwrite('matches/flag_piece' + str(fc_count) + '.png', flag_piece)
		fc_count += 1
		ic_count = 0
		for ic in img_bits:
			rot = 0
			while(rot < 360):
				template = rotate(flag_piece, rot)
				result = cv2.matchTemplate(ic[1], template, cv2.TM_SQDIFF_NORMED)
				if(result < 0.55):
					cv2.imwrite('matches/b' + str(count) + '_pattern.png', ic[1])
					cv2.imwrite("matches/b"+str(count)+"_color.png", ic[0])
					cv2.imwrite("matches/b"+str(count)+"_" + str(result) + "_flag.png", template)
					count += 1
					if(count >= 2):
						return True
			
				rot += 10
			ic_count += 1
	return False


if __name__ == "__main__":
	#check the number of command line args
	#expect the first argument to be path of image being checked
	if(len(sys.argv) <= 1):
		print "No image specified. Use './flagfinder image'."
		exit()
	
	if detect_flag_method1(sys.argv[1]) or detect_flag_method2(sys.argv[1]):
		print "Possible flag found"
		exit(1)
	print "Seems ok"
	exit(0)
