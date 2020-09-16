#!/usr/bin/env python3
from selenium import webdriver
import tkinter as tk
import time
import argparse
#import getpass
import os

languages = {
				"PYTH"     : ".py",
				"PYTH 3.6" : ".py",
				"C++14"    : ".cpp",
				"C++17"	   : ".cpp",
				"JAVA"     : ".java",
				"C"        : ".c"	
			}

def Clipboard():
	root = tk.Tk()
	root.withdraw()
	return root.clipboard_get()

def main(username, password, user): 
	driver = webdriver.Chrome()
	driver.maximize_window()
	url = "https://www.codechef.com"
	driver.get(url)
	#username = input("Username: ")
	#password = getpass.getpass()
	#user = input("User: ")
	driver.find_element_by_name("name").send_keys(username)
	driver.find_element_by_name("pass").send_keys(password)
	driver.find_element_by_name("op").click()
	time.sleep(1)

	if driver.current_url == url:
		print("Login Failed")
		driver.quit()

	driver.get("https://www.codechef.com/users/"+user)
	code_links = []
	submissions = driver.find_elements_by_tag_name("a")
	for sub in submissions:
		link = sub.get_attribute("href")
		if link is not None and "status" in link and link.endswith(user):
			code_links.append(link)

	count = 0
	problem_name = source = ""
	for link in code_links:
		driver.get(link)
		time.sleep(3)
		try:
			status = driver.find_elements_by_xpath('//*[@id="primary-content"]/div/div[3]/table/tbody/tr/td[4]/span/img')
			langs = driver.find_elements_by_xpath('//*[@id="primary-content"]/div/div[3]/table/tbody/tr/td[7]')
			status_links = driver.find_elements_by_xpath('//*[@id="primary-content"]/div/div[3]/table/tbody/tr/td[8]/ul/li/a')
		except:
			print("Oops!!! Some error in Submission Page")

		problem_link = driver.find_elements_by_xpath('//*[@id="breadcrumb"]/div/a')
		for prob in problem_link:
			if "problems" in prob.get_attribute("href"):
				problem_name = prob.text.strip()

		for i in range(len(status)):
			if "tick-icon" in status[i].get_attribute("src"):
				lang = langs[i].text.strip()
				user_path = os.path.join(os.getcwd(), "Codechef", user)
				prob_path = os.path.join(user_path, problem_name + languages.get(lang, ".txt"))
				if os.path.exists(prob_path) == False:
					try:
						driver.get(status_links[i].get_attribute("href"))
						time.sleep(3)
						driver.find_element_by_id('copy-button').click()
						source = Clipboard()
					except:
						print("Oops!!! Some error in Code Page")
				else:
					print("File Already Existed!")

				if len(source) > 0:
					if not os.path.exists(user_path):
						os.makedirs(user_path)
					f = open(prob_path, 'w+')
					f.write(source)
					f.close()
			break

		count+=1
		print("[{:{}}] {:.1f}%".format("="*count, len(code_links)-1, (100/(len(code_links)-1)*count)))
	
	driver.quit()

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Codechef Submission Scraper")
	parser.add_argument("-u", "--username", help="[+] Input Username")
	parser.add_argument("-p", "--password", help="[+] Input Passowrd")
	parser.add_argument("-U", "--USER", help="[+] Input username to scrape")
	args = parser.parse_args()
	main(args.username, args.password, args.USER)


