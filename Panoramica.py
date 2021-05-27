#import the necessary packages
from imutils import paths
import numpy as np
import imutils
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str, required=True,
    help = "ruta del video de origen")
ap.add_argument("-t", "--time", type=float, required=True,
    help = "Tiempo entre de separación entre cada captura (en segundos)")
ap.add_argument("-o", "--output", type=str, required=True,
	help="path to the output image")
args = vars(ap.parse_args())

vidcap = cv2.VideoCapture(args["video"])
tiempo = args["time"]

FPS = int(vidcap.get(cv2.CAP_PROP_FPS))
tiempo_fotogram = 1/FPS
count = 0
foto = 0

width = 1280
height = 720
dimensions = (width, height)
print("[INFO] Extrayendo fotogramas...")

while vidcap.isOpened():
    success, image = vidcap.read()

    if success:
        count += tiempo_fotogram
        image_resized = cv2.resize(image,dimensions, interpolation=cv2.INTER_AREA)

        if count > tiempo:
            cv2.imwrite("Frames/frame%d.jpg" % foto, image)     # save frame as JPEG file
            foto +=1
            count = 0
            
    else:
        break

vidcap.release()
print("[INFO] ",foto," fotogramas extraidos...")

# grab the paths to the input images and initialize our images list
print("[INFO] loading images...")
imagePaths = sorted(list(paths.list_images("Frames/")))
images = []
# loop over the image paths, load each one, and add them to our
# images to stitch list
for imagePath in imagePaths:
    image = cv2.imread(imagePath)
    images.append(image)


# initialize OpenCV's image stitcher object and then perform the image
# stitching
print("[INFO] stitching images...")
stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
(status, stitched) = stitcher.stitch(images)

# if the status is '0', then OpenCV successfully performed image
# stitching
if status == 0:
    print("[INFO] Image stitching exitoso")
    cv2.imwrite(args["output"], stitched)
    cv2.imshow("Stitched", stitched)
    cv2.waitKey(0)
else:
	print("[INFO] image stitching failed ({})".format(status))
    
