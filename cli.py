#!/usr/bin/env python

import os, sys, getopt
from filetoimage import encode, decode


def do_encode(argv):
	help_str = "usage: cli.py encode <input_file_path> <output_img_dir> [-chunk_size=<bytes>]"
	if len(argv) < 2:
		print help_str
		sys.exit(2)  # exit code 2 signifies command line syntax error
	input_file_path = argv[0]
	output_img_dir = argv[1]
	try:
		
	encode(input_file_path, output_img_dir)


def do_decode(argv):
	help_str = "usage: cli.py decode <input_file_name> <input_image_dir> <outfile_dir> <num_chunks>"
	if len(argv) < 4:
		print help_str
		sys.exit(2)
	input_file_name = argv[0]
	input_image_dir = argv[1]
	outfile_dir = argv[2]
	num_chunks = argv[3]
	decode(input_file_name, input_image_dir, outfile_dir, num_chunks)


def main(argv):
	"""
	Usage:  cli.py encode <input_file_path> <output_img_dir>
	or
			cli.py decode <input_file_name> <input_image_dir> <outfile_dir> <num_chunks>
	"""
	help_str = 'Usage: cli.py encode -i <input_file_path|directory> -o <output_img_dir>'

	# try:
	# 	opts, args = getopt.getopt(argv, 'hi:o:')
	# except getopt.GetoptError:
	# 	print help_str
	# 	sys.exit(2)

	command = argv[0].lower()
	print "Command:", command
	if command == "encode":
		do_encode(argv[1:])
	elif command == "decode":
		do_decode(argv[1:])
	elif command == "help":
		commands = ["encode", "decode", "help"]
		help_str = "usage: cli.py <command> [options]\n\ncommands: %s" % ", ".join(commands)
		print help_str
		sys.exit()

	# for opt, arg in opts:
	# 	print "opt:", opt
	# 	if opt == '-h':
	# 		print help_str
	# 		sys.exit()
	# 	# elif opt == "-i":
	# 	# 	input_file_path = arg
	# 	# elif opt == "-o":
	# 	# 	output_img_dir = arg
	# for arg in args:
	# 	print "arg:", arg


if __name__ == "__main__":
	main(sys.argv[1:])
