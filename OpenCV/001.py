import cv2

# Canny edge detection

cat = cv2.imread("Data/cat.jpg")
cv2.imshow("original", cat)
cv2.waitKey(0)

cat = cv2.GaussianBlur(cat, (5, 5), 0)
cv2.imshow("blurred", cat)
cv2.waitKey(0)

edges = cv2.Canny(cat, 50, 200) # second and third values are min and max of intensity gradient
cv2.imshow("edges", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
