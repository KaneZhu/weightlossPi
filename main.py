import cv2
import numpy as np

#structing element with 3*3 elements
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
code=0
img = cv2.imread("3.jpg",0)	#change grey
res = cv2.resize(img,None,fx=.3,fy=.3,interpolation=cv2.INTER_CUBIC)
# res = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)  #change grey, however 'img = cv2.imread("2.jpg",0)'has changed
# cv2.namedWindow("orignial image")
# # cv2.imshow("orignial image",res)

eroded = cv2.erode(res,kernel)
# cv2.namedWindow("eroded image")
# # cv2.imshow("eroded image",eroded)
dilated = cv2.dilate(res,kernel)
# cv2.namedWindow("dilated image")
# cv2.imshow("dilated image",dilated)

result = cv2.absdiff(dilated,eroded)
result = cv2.bitwise_not(result)
#cv2.namedWindow("diff result")
#cv2.imshow("diff result",result)

ret,img2=cv2.threshold(result,127,255,cv2.THRESH_BINARY)
result = cv2.bitwise_not(result)
cv2.namedWindow("img2_1")
cv2.imshow("img2_1",img2)


img2 = cv2.erode(img2, None, iterations = 4)
img2 = cv2.dilate(img2, None, iterations = 4)
img2 = cv2.bitwise_not(img2)
#cv2.namedWindow("img2_4")
#cv2.imshow("img2_4",img2)

(cnts, _) = cv2.findContours(img2.copy(), cv2.RETR_EXTERNAL,
cv2.CHAIN_APPROX_SIMPLE)
c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]

# compute the rotated bounding box of the largest contour
rect = cv2.minAreaRect(c)
box = np.int0(cv2.cv.BoxPoints(rect))
print box

# draw a bounding box arounded the detected barcode and display the
# image
# cv2.drawContours(res, [box], -1, (0, 255, 0), 3)
#cv2.namedWindow("image")
# cv2.imshow("image", res)

pts1 = np.float32([box[2],box[3],box[1],box[0]])
pts2 = np.float32([[0,0],[500,0],[0,300],[500,300]])

M = cv2.getPerspectiveTransform(pts1,pts2)

dst = cv2.warpPerspective(res,M,(500,300))

#cv2.bitwise_not(dst)

cv2.namedWindow("final")
cv2.imshow("final",dst)
#GaussianBlur
dst = cv2.GaussianBlur(dst,(5,5),1.5)
# binary
ret,dst=cv2.threshold(dst,100,255,cv2.THRESH_BINARY)
cv2.namedWindow("Final_2")
cv2.imshow("Final_2",dst)

#gain the shap of the cutted pic

m, n = dst.shape[:2]
bar_y = np.zeros((500,255))
l=0
for i in range(1,m):
    k = 1
    l = l+1
    for j in range(1,n-1):
        if dst[i,j]!=dst[i,j+1]:
            #bar_x(l,k) = i
            bar_y[l,k]=j
            k = k+1
        if k>61:
            l = l-1
            break
    if k<61:
        l = l-1

print bar_y


m, n = bar_y.shape[:2]

if m <= 1:
    code = '0'
    print(1,'GameOver!\n')
    

for i in range(1,m):           
    for j in range(1,n-1):
        bar_num[i,j] = bar_y[i,j+1] - bar_y[i,j]
        if bar_num[i,j]<0:
            bar_num[i,j] = 0
        
    

bar_sum = sum(bar_num)/m   
k = 0
for i in range(1,59):   
    k = k + bar_sum[i]

k = k/95   
for i in range(1,59): 
    bar_int[i] = round(bar_sum[i]/k)

k = 1
for i in range(1,59):  
    if rem in range(i,2):
        for j in range(1,bar_int[i]):  
            bar_01[k] = 1
            k = k+1
        
    else:
        for j in range(1,bar_int[i]):  
            bar_01[k] = 0
            k = k+1
        
    



cv2.waitKey(0)
cv2.destroyAllWindows()