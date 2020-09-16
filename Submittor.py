#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.support.ui import Select
import argparse
import time

languages = {
				"Py2"      : "4",
				"Py3"      : "116",
				"C++14"    : "44",
				"C++17"	   : "63",
				"Java"     : "10",
				"C"        : "11"	
			}

def Sleep(t):
	return time.sleep(t)

def main(username, password, problem, lang, file): 
	driver = webdriver.Chrome()
	driver.maximize_window()
	url = "https://www.codechef.com"
	driver.get(url)
	#username = input("Username: ")
	#password = getpass.getpass()
	driver.find_element_by_name("name").send_keys(username)
	driver.find_element_by_name("pass").send_keys(password)
	driver.find_element_by_name("op").click()
	submit_url = "https://www.codechef.com/submit/"+problem
	driver.get(submit_url)
	Sleep(3)
	driver.find_element_by_id("edit-submit").click()
	with open(file, "r") as f:
		source = f.read()
	driver.find_element_by_xpath('//*[@id="edit-program-wrapper"]/textarea').send_keys(source)
	select = Select(driver.find_element_by_id('edit-language'))
	select.select_by_value(languages.get(lang))
	driver.find_element_by_id("edit-submit-1").click()
	Sleep(5)

	driver.quit()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Codechef Code Submitter")
	parser.add_argument("-u", "--username", help="[+] Input Username")
	parser.add_argument("-p", "--password", help="[+] Input Passowrd")
	parser.add_argument("-t", "--problem",  help="[+] Input Problem")
	parser.add_argument("-l", "--lang",     help="[+] Input Language")
	parser.add_argument("-f", "--file",     help="[+] Input Source File")
	args = parser.parse_args()
	main(args.username, args.password, args.problem, args.lang, args.file)