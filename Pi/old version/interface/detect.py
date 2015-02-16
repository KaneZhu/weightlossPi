import cv2
import numpy as np
import json, urllib2
def detect():
   #structing element with 3*3 elements
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
	code='0'
	img = cv2.imread("6.jpg",0) #change grey
	res = cv2.resize(img,None,fx=.3,fy=.3,interpolation=cv2.INTER_CUBIC)

	eroded = cv2.erode(res,kernel)
	dilated = cv2.dilate(res,kernel)
	# cv2.namedWindow("dilated image")
	# cv2.imshow("dilated image",dilated)

	result = cv2.absdiff(dilated,eroded)
	result = cv2.bitwise_not(result)
	# cv2.namedWindow("diff result")
	# cv2.imshow("diff result",result)

	ret,img2=cv2.threshold(result,127,255,cv2.THRESH_BINARY)
	img2 = cv2.erode(img2, None, iterations = 4)
	img2 = cv2.dilate(img2, None, iterations = 4)
	img2 = cv2.bitwise_not(img2)
	# cv2.namedWindow("img2_4")
	# cv2.imshow("img2_4",img2)

	(cnts, _) = cv2.findContours(img2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]

	# compute the rotated bounding box of the largest contour
	rect = cv2.minAreaRect(c)
	box = np.int0(cv2.cv.BoxPoints(rect))
	#draw a bounding box arounded the detected barcode and display the image
	# cv2.drawContours(res, [box], -1, (0, 255, 0), 3)
	# cv2.namedWindow("image")
	# cv2.imshow("image", res)

	#########################################################################
	#adjust the box sequence
	box_r=np.zeros((4,2),dtype=int)
	tempbox=np.zeros((1,2),dtype=int)
	box_r[3]=box[3]
	#find max x and give it to r[3]
	for i in range (0,4):
	    if box_r[3][0] < box [i][0]:
	        box_r[3]=box[i]
	#find second max x and give it to r[1]
	for i in range (0,4):
	    if box_r[1][0] < box [i][0] and box[i][0]!= box_r[3][0] and box[i][1]!= box_r[3][1]:
	        box_r[1]=box[i]
	#check r1 r3
	if box_r[1][1] > box_r[3][1]:
	    tempbox[0][0]=box_r[1][0]
	    tempbox[0][1]=box_r[1][1]
	    box_r[1]=box_r[3]
	    box_r[3]=tempbox
	#find min x and give it to r[0]
	box_r[0]=box_r[3]
	box_r[2]=box_r[3]
	for i in range (0,4):
	    if box_r[0][0] > box [i][0]:
	        box_r[0]=box[i]
	#find second max x and give it to r[2]
	for i in range (0,4):
	    if box_r[2][0] > box [i][0] and box[i][0]!= box_r[0][0] and box[i][1]!= box_r[0][1]:
	        box_r[2]=box[i]
	#check r0 r2
	if box_r[0][1] > box_r[2][1]:
	    tempbox[0][0]=box_r[0][0]
	    tempbox[0][1]=box_r[0][1]
	    box_r[0]=box_r[2]
	    box_r[2][0]=tempbox[0][0]
	    box_r[2][1]=tempbox[0][1]
	print box_r
	###################################################################################
	#adjust the pic
	pts1 = np.float32([box_r[0],box_r[1],box_r[2],box_r[3]])
	pts2 = np.float32([[0,0],[500,0],[0,300],[500,300]])
	M = cv2.getPerspectiveTransform(pts1,pts2)
	dst = cv2.warpPerspective(res,M,(500,300))

	#cv2.bitwise_not(dst)
	##    cv2.namedWindow("final")
	##    cv2.imshow("final",dst)
	#GaussianBlur
	dst = cv2.GaussianBlur(dst,(5,5),1.5)

	#binary
	ret,dst=cv2.threshold(dst,100,255,cv2.THRESH_BINARY)
	# cv2.namedWindow("Final_2")
	# cv2.imshow("Final_2",dst)

	#gain the shap of the cutted pic
	#variable define:
	m,n = dst.shape[:2]
	# print('m=',m,',n=',n)
	bar_y = np.zeros((500,300),dtype=int)
	bar_num = np.zeros((500,300))
	l=0
	length_1=0
	hight_1=0
	for i in range(1,m):
	    k = 1
	    l = l+1
	    for j in range(1,n-1):
	        #compare two color of conjuction points
	        if dst[i,j]!=dst[i,j+1]:
	            #bar_x(l,k) = i
	            bar_y[l-1,k-1]=j    #record the changing point /////minus 1
	            k = k+1             #moving to the next point
	        if k>61:
	            l = l-1
	            break
	    if k<61:
	        l = l-1

	    #save the biggest matrix range
	    if length_1<l-1:
	        length_1=l-1;
	    if hight_1<k-1:
	        hight_1=k-1;


	# print length_1,hight_1
	# print bar_y
	#cutting the oversized simpling matrix
	bar_yy = np.zeros((length_1,hight_1),dtype=int) #define the temp matrix
	for i in range(0,length_1):
	    for j in range(0,hight_1):
	        bar_yy[i,j]=bar_y[i,j]
	# np.delect(bar_y,[0],None)
	bar_y=bar_yy
	# print bar_y

	# print(length_1,hight_1)
	m,n = bar_y.shape[:2]
	# print('m=',m,',n=',n)

	if m <= 1:
	    code = '0'
	    print(1,'GameOver~\n')
	    
	#the length of each bar
	for i in range(0,m):           
	    for j in range(0,n-1):
	        bar_num[i,j] = bar_y[i,j+1] - bar_y[i,j]
	        if bar_num[i,j]<0:
	            bar_num[i,j] = 0
	#cutting bar_num
	bar_num_temp = np.zeros((m,n-1)) #define the temp matrix
	for i in range(0,m):
	    for j in range(0,n-1):
	        bar_num_temp[i,j]=bar_num[i,j]
	bar_num=bar_num_temp

	# print bar_num.shape[:2]
	# print bar_num[223,58]
	#average length of each bar
	sum_bar_num=np.zeros(n-1)
	for i in range(0,m-1):
	    for j in range(0,n-1):
	        sum_bar_num[j]=sum_bar_num[j]+bar_num[i,j]
	bar_sum = sum_bar_num/m    
	# print (bar_sum)

	k = 0
	for i in range(0,59):   #total length of bar  
	    k = k + bar_sum[i]

	bar_int = np.zeros(n-1,dtype=int)  
	k = k/97    #the length of unit bar
	for i in range(0,59): 
	    bar_int[i] = round(bar_sum[i]/k)
	# print bar_int

	#change to binary
	binary_bar = np.zeros(95,dtype=int)
	k = 0
	for i in range(0,59):  
	    if i%2 == 0:
	        for j in range(0,bar_int[i]):  
	            binary_bar[k] = 1   #dark is 1
	            k = k+1
	        
	    else:
	        for j in range(0,bar_int[i]):  
	            binary_bar[k] = 0   #white is 0
	            k = k+1
	# print binary_bar
	    
	#########################
	#start to change the binary codes in to bar codes
	#
	check_left = np.int0([[13,25,19,61,35,49,47,59,55,11],[39,51,27,33,29,57, 5,17, 9,23]])
	check_right = np.int0([114,102,108,66,92,78,80,68,72,116])
	first_num = np.int0([31,20,18,17,12,6,3,10,9,5])
	bar_left = np.zeros(6,dtype=int)
	bar_right = np.zeros(6,dtype=int)
	if ((binary_bar[0] and ~binary_bar[1] and binary_bar[2]) and (~binary_bar[45] and binary_bar[46] and ~binary_bar[47] and binary_bar[48] and ~binary_bar[49]) and (binary_bar[94] and ~binary_bar[93] and binary_bar[92])):
	    l = 0
	    #change the left binary numbers into decimal numbers
	    for i in range(1,7):
	        bar_left[l] = 0
	        for k in range(1,8):
	            bar_left[l] = bar_left[l]+(binary_bar[7*(i-1)+k+2])*(2**(7-k))
	        l = l+1
	    
	    l = 0
	    #change the right binary numbers into decimal numbers
	    for i in range(1,7):
	        bar_right[l] = 0
	        for k in range(1,8):
	            bar_right[l] = bar_right[l]+binary_bar[7*(i+6)+k]*(2**(7-k))
	            k = k-1
	        l = l+1

	num_bar = ''
	num_first = 0
	first = 2
	#check the bar codes from the left bar dictionary
	for i in range(1,7):
	    for j in range(0,2):
	        for k in range(0,10):
	            if bar_left[i-1]==check_left[j,k]:
	                # num_bar = strcat(num_bar , num2str(k));
	                num_bar += str(k)
	                # print num_bar
	                if first == 0:
	                    if j==0:
	                        num_first = num_first + (2**(6-i))
	                elif first == 1:
	                    num_first = num_first + j*(2**(6-i))
	                    print num_first
	                elif first == 2:
	                    first = j


	#check the bar codes from the right bar dictionary
	for i in range(1,7):
	    for j in range(0,10):
	        if bar_right[i-1]==check_right[j]:
	            num_bar += str(j)
	            # num_bar = strcat(num_bar , num2str(j))

	#check first bar code from the first bar code dictionary
	for i in range(0,10):
	    if num_first==first_num[i]:
	        num_bar = str(i)+num_bar
	        # num_bar = strcat(num2str(i) , num_bar)
	        break

	print 'the bar code is: ',num_bar

	url='http://10.0.2.11:9393/foods.json?barcode='+num_bar
	print url
	r=urllib2.urlopen(url)
	json_string=r.read()
	userdata=json.loads(json_string)
	return userdata
	
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()