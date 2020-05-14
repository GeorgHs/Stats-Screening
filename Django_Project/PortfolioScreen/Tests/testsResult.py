import unittest
import xmlrunner

def runner(output='python_tests_xml'):
	return xmlrunner.XMLTestRunner(
		outpute=output
	)
def find_tests():
	return unittest.TestLoader().discover('pystache')

if __name__== '__main__':
	runner().run(find_tests())
