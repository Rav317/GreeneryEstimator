import cv2
import os
import csv
import time



def load_images_from_folder(folder):
	images = {}
	for filename in os.listdir(folder):

		img = cv2.imread(os.path.join(folder,filename))
		
		current_sector = filename.replace(".png","")
		
		if img is not None:
			images[current_sector] = img

	return images


if __name__ == '__main__':

	# Start the clock
	start_time = time.time()

	# Path to the image directory
	path = os.path.join("images","satellite")

	# Image resolution : 256 x 256 pixels
	TOTAL_PIXELS = 65536

	# Filepath
	file_path = os.path.join("csv","greenery_percentage.csv")

	# File handling
	f = open(file_path, mode = "w", newline = '')
	f_wr = csv.writer(f, delimiter = ",", quoting = csv.QUOTE_MINIMAL)
	f_wr.writerow(['Sector', "Percentage Green"])


	# A dictionary of images with key as sectorname
	# Eg : image_list["sector30"]
	image_list = load_images_from_folder(path)


	for sector, img in image_list.items():

		print("Sector : ", sector)

		green_pixel_count = 0

		for i in img:
			for j in i:

				if(j[1]>j[0] and j[1]>j[2] and j[0]<100 and j[2]<100):
					green_pixel_count += 1

		greenery_percentage = green_pixel_count*100/TOTAL_PIXELS
		
		# Find greenery | Keep lake bias check
		if(greenery_percentage > 60):

			roadmap_img = cv2.imread(os.path.join("images","roadmap",sector+".png"))
			lake_pixel_count = 0

			for i in roadmap_img:
				for j in i:


					# rgb(178, 207, 242)
					if(j[0] == 242 and j[1] == 200 and j[2] == 172):
						lake_pixel_count += 1

			if(lake_pixel_count > 0):
				green_pixel_count -= lake_pixel_count
				print("-----------------percent count changed for sector : ",sector)

		# Find greenery percentage
		greenery_percentage = green_pixel_count*100/TOTAL_PIXELS


		# Enter data in file
		f_wr = csv.writer(f, delimiter = ",", quoting = csv.QUOTE_MINIMAL)
		f_wr.writerow([sector,greenery_percentage])
			

	f.close()
	print("--- %s seconds ---" % (time.time() - start_time))

