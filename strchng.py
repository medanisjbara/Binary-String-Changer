#!/usr/bin/env python3
import argparse, os, sys

def handle(f):
	def wrapper(*arg,**kwargs):
		if args.e:
			try:
				f(*arg,**kwargs)
			except:
				print ('File skipped')
				print ('proceeding ...')
				print ()
		else:
			f(*arg,**kwargs)
	return wrapper

@handle
def convert (input,output=None,old=None,new=None):
	with open (input,'rb') as file:
		content = file.read().replace(args.old_string.encode(),args.new_string.encode())
	if output == None:
		output=input
	with open (output,'wb') as file:
		file.write(content)
	return True

def override (input):
	for r, d, f in os.walk(input):
		for file in f:
			convert (os.path.join(r,file))
		for folder in d:
			override (os.path.join(r,folder))

def dir_to_dir (input,output):
	if not os.path.exists(output):
		os.mkdir(output)
	for r,d,f in os.walk(input):
		for dir in d:
			dir =os.path.join(r.replace(input,output),dir)
			if not os.path.exists(dir):
				os.mkdir(dir)
		for file in f:
			temp_input=os.path.join(r,file)
			temp_output=os.path.join(r.replace(input,output),file)
			convert (temp_input,temp_output)


if __name__=="__main__":
	parser = argparse.ArgumentParser(
	description="""This program was initially made to chages termux binaries to work on pydroid or other terminals
	example: strchng -i a.out -o output -old "Hello World" -new "Goodbye Everyone" """)
	parser.add_argument('-i','--input',metavar='',help="The input file or folder",required=True)
	parser.add_argument('-o','--output',metavar='',help="The output file or folder",default=None)
	parser.add_argument('-old','--old-string',metavar='' ,help="The old string that you want to replace",default='com.termux/files')
	parser.add_argument('-new','--new-string',metavar='' ,help="The new string that will be replaced",default='ru.iiec.pydroid/usr')
	parser.add_argument('-e',help='Ignore errors',action='store_true')
	if len(sys.argv)==1:
		parser.print_help(sys.stderr)
		sys.exit(1)
	args = parser.parse_args()
	input=os.path.join(os.getcwd(),args.input)
	if os.path.isdir(input):
		if args.output==None:
			override(input)
		else:
			output = os.path.join(os.getcwd(),args.output)
			if output [-1]!="/":
				output+="/"
			dir_to_dir(input,output)
	else:
		convert(input,args.output)

