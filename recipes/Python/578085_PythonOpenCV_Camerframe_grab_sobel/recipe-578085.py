import cv2.cv as cv

cv.NamedWindow("camera", 1)
capture = cv.CaptureFromCAM(0)

while True:
    img = cv.QueryFrame(capture)
    im_gray  = cv.CreateImage(cv.GetSize(img),cv.IPL_DEPTH_8U,1)
    cv.CvtColor(img,im_gray,cv.CV_RGB2GRAY)
    
    
    # Sobel operator
    dstSobel = cv.CreateMat(im_gray.height, im_gray.width, cv.CV_32FC1)
    # Sobel(src, dst, xorder, yorder, apertureSize = 3)
    cv.Sobel(im_gray,dstSobel,1,1,3)
    cv.ShowImage('camera', dstSobel)
    
    
    # image smoothing and subtraction
#    imageBlur = cv.CreateImage(cv.GetSize(im_gray), im_gray.depth, im_gray.nChannels)
#    # filering the original image
#    # Smooth(src, dst, smoothtype=CV_GAUSSIAN, param1=3, param2=0, param3=0, param4=0)
#    cv.Smooth(im_gray, imageBlur, cv.CV_BLUR, 11, 11)
#    diff = cv.CreateImage(cv.GetSize(im_gray), im_gray.depth, im_gray.nChannels)
#    # subtraction (original - filtered)
#    cv.AbsDiff(im_gray,imageBlur,diff)
#    cv.ShowImage('camera', diff)
    
    if cv.WaitKey(10) == 27:
        break
cv.DestroyWindow("camera")
