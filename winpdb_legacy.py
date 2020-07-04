import sys

def main():
	msg = 'The debugger `winpdb` is now developed under the package name `winpdb-reborn`\n'
	msg += 'It has been installed along with this package.\n'
	msg += '\n'
	msg += 'To launch winpdb, use: python -m winpdb\n'
	msg += '\n'
	msg += 'To get updates of the debugger `winpdb`, update the package `winpdb-reborn`.\n'
	print(msg)
	sys.exit(-1)


if __name__ == '__main__':
	main()