import os, sys, getopt
import math
import numpy, Image, struct
import pdb


def encode(input_file_path, output_img_dir, chunk_size=1048576):
	with open(input_file_path) as f:
		check_or_create_dir(output_img_dir)
		input_file_name = os.path.split(input_file_path)[1]
		size = get_file_size(input_file_name)
		print "File size:", size, "bytes."
		num_chunks = get_num_chunks(input_file_name, chunk_size)
		print "Number of chunks:", num_chunks

		for chunk in range(num_chunks):
			print "Encoding image", (chunk+1), "of", num_chunks

			# Compute the actual size of this chunk (could be smaller if the last one)
			curr_size = min(chunk_size, size-f.tell())
			width = height = int(math.ceil(math.sqrt(curr_size/3)))
			print "Image size:", str(width)+"x"+str(height), "pixels"

			a = numpy.zeros((height, width, 4))

			for i in range(height):
				for j in range(width):
					# Keep track of the number of bytes actually stored in this pixel
					num_bytes_in_pixel = 0
					for k in range(3):
						c = f.read(1)
						if not c:
							continue
						val = struct.unpack('B', c)[0]
						num_bytes_in_pixel += 1
						a[i, j, k] = val
					# Store how many bytes in this pixel in the 'A' channel of the pixel
					a[i, j, 3] = num_bytes_in_pixel
					# if num_bytes_in_pixel == 0: print "no bytes in this pixel:", i, j

			im = Image.fromarray(a.astype('uint8')).convert('RGBA')
			im.save(get_img_path(output_img_dir, input_file_name, chunk))

		return num_chunks


def decode(input_file_name, input_image_dir, outfile_dir, num_chunks):
	check_or_create_dir(outfile_dir)

	# Make sure input_file_name is just the name, not a path
	input_file_name = os.path.split(input_file_name)[1]

	outfile_path = os.path.join(outfile_dir, input_file_name)
	print "outfile_path:", outfile_path
	# if os.path.exists(outfile_path):
	# 	# Don't overwrite some existing file
	# 	print "The output path already exists:", outfile_path
	# 	sys.exit()

	print "input_file_name:", input_file_name

	outfile = open(outfile_path, 'wb')
	outfile.write("")

	with open(outfile_path, 'a+b') as outfile:
		print "got here 2"
		for chunk in range(num_chunks):
			print "Decoding image", (chunk+1), "of", num_chunks
			print "img_path", get_img_path(input_image_dir, input_file_name, chunk)
			im = Image.open(get_img_path(input_image_dir, input_file_name, chunk))
			pixels = im.load()
			width, height = im.size
			for i in range(height):
				for j in range(width):
					pixel = pixels[j, i]
					num_bytes_in_pixel = pixel[3]  # get num bytes from the 'A' channel of RGBA
					# if num_bytes_in_pixel == 0: print "no bytes in this pixel:", i, j
					for k in range(num_bytes_in_pixel):
						# print k
						byte = struct.pack('B', pixel[k])
						outfile.write(byte)


def encode_dir(input_dir, output_img_dir, chunk_size=1048576):
	if os.path.isdir(input_dir):
		# encode all files in directory
		files = [ f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f)) ]
		for file_path in files:
			encode(file_path, output_img_dir, chunk_size)
	elif os.path.exists(input_dir):
		# this is a file, so just encode this file
		encode(input_dir, output_img_dir, chunk_size)
	else:
		print "This path doesn't exist."
		sys.exit()


def get_img_path(img_dir, input_file_name, img_num):
	"""
	Computes the name of the encoded image
	"""
	PREFIX = "flickrstore"
	# pdb.set_trace()
	img_name = '%s_%s_%000d.png' % (PREFIX, input_file_name, img_num)
	img_path = os.path.join(img_dir, img_name)
	print "image name:", img_path
	return img_path


def get_file_size(path):
	"""
	Given the filename, return the size of the file in bytes
	"""
	return os.path.getsize(path)


def check_or_create_dir(directory):
	"""
	Make sure directory exists and isn't a file, otherwise create directory
	"""
	if os.path.exists(directory) and not os.path.isdir(directory):
		print "Directory provided is a file"
		sys.exit()
	if not os.path.exists(directory):
		print "Creating directory for images:", directory
		os.makedirs(directory)


def get_num_chunks(path, chunk_size):
	"""
	Compute the number of chunks this file will be split up into
	path -> the name of the file
	chunk_size -> the size of each chunk in bytes
	"""
	return max(1, int(math.ceil(get_file_size(path) * 1.0 / chunk_size)))


def compare_files(f1name, f2name):
	with open(f1name) as f1:
		with open(f2name) as f2:

			size1 = os.path.getsize(f1name)
			size2 = os.path.getsize(f2name)
			if size1 != size2:
				print "The files are different sizes!"
				return

			# Compare the bytes
			for i in range(size1):
				c1 = f1.read(1)
				c2 = f2.read(1)
				if c1 != c2:
					print "The characters at", str(i), "are not the same:", c1, c2
					return

			print "The files are the same!"


def test():
	# Split files into chunks of this size (bytes)
	# 1073741824 = 1 gig
	chunk_size = 1048576  # 1 MB

	input_file_name = './wild dogs safari.jpg'
	outfile_dir = './decoded/'
	img_dir = './images'

	num_chunks = encode(input_file_name, img_dir, chunk_size)
	print "***DECODING***"
	decode(input_file_name, img_dir, outfile_dir, num_chunks)

	outfile_path = os.path.join(outfile_dir, input_file_name)

	compare_files(input_file_name, outfile_path)


if __name__ == "__main__":
	test()
