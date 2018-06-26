# Video-Doc-Scanner
Scans a document 
To scan a document video feed is taken
Camera resolution is set to full HD
Edges are sharpened using gaussian HPF
After simple preprocessing canny edge detection is used to detect the edges, kenny parameters can be changed for better results
Contours are detected in the edge image, contours min area is defined and polygons with four vertices and significant area is only selected
Image is resalligned using perpective transform and stored
Thresholding can be used for black and white scanned images
