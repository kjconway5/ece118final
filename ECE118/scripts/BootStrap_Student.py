import subprocess
import sys

PackagesNeeded=['requests',  'PyQT5', 'pyserial', 'lxml', 'pcpp', 'pycparser', 'saxonche']

for package in PackagesNeeded:
	print('Installing '+package)
	subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', package], check=True)
