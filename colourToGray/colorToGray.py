import cv2

image_convert = cv2.imread('C:\\Users\\ashoka\\Documents\\s_d\\Rose_flower.jpg',
                           cv2.IMREAD_UNCHANGED)

g = cv2.cvtColor(image_convert, cv2.COLOR_BGR2GRAY)

thresh, black = cv2.threshold(g , 170, 255, cv2.THRESH_BINARY)

cv2.imshow("Black Image", black)
cv2.imwrite('im_grayscale.png',g)
cv2.imwrite('image_black.png',black)

cv2.waitKey(0)
cv2.destroyAllWindows()
