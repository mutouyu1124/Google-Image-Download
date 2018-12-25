import sys
import urllib2
from urllib2 import Request, urlopen, URLError, HTTPError
from urllib import quote
import httplib
from httplib import IncompleteRead
httplib._MAXHEADERS = 1000
import time
import os
import argparse
import ssl
import datetime
import json
import re
import codecs
import socket

args_list = ["keywords","url","limit","format","color_type","size",
			 "type","output_directory","image_directory","chromedriver","safe_search","print_urls"]
def user_input():
	parser = argparse.ArgumentParser()
	parser.add_argument("-k", "--keywords",help = "delimited list input", type = str, required = False)
	parser.add_argument("-u", "--url", help = "search with google image URL", type = str, required = False)
	parser.add_argument("-l", "--limit", help = "delimited list input",type = str, required = False)
	parser.add_argument("-f", "--format", help = "download images with specific format", type = str, required = False, choices = ['jpg','gif','png','bmp','svg'])
	parser.add_argument("-ct","--color_type", help = "filter on color",type = str, required = False, choices = ['full-color','black-and-white','transparent'])
	parser.add_argument("-s", '--size', help='image size', type=str, required=False,choices=['large','medium','icon','>400*300','>640*480','>800*600','>1024*768','>2MP','>4MP','>6MP','>8MP','>10MP','>12MP','>15MP','>20MP','>40MP','>70MP'])
	parser.add_argument("-t", "--type", help = "image type", type = str, required = False)
	parser.add_argument("-o", "--output_directory", help = "downloading images in a specific main directory",type = str, required = False)
	parser.add_argument("-i", "--image_directory", help = "download images in a specific sub-directory", type = str, required = False)
	parser.add_argument("-sa", "--safe_search", default=False, help="Turns on the safe search filter while searching for images", action="store_true")
	parser.add_argument("-cd", "--chromedriver", help='specify the path to chromedriver executable in your local machine', type=str, required=False)
	parser.add_argument("-p","--print_urls", help = "Print the URLs of the images", action = "store_true")
	args = parser.parse_args()
	arguments = vars(args)
	records = []
	records.append(arguments)
	return records

class googleimagesdownload():
	def __init__(self):
		pass

	def creat_directories(self, main_directory, dir_name):
		try:
			if not os.path.exists(main_directory):
				os.makedirs(main_directory)
				time.sleep(0.2)
				path = str(dir_name)
				sub_directory = os.path.join(main_directory,path)
				if not os.path.exists(sub_directory):
					os.makedirs(sub_directory)
			else:
				path = str(dir_name)
				sub_directory = os.path.join(main_directory,path)
				if not os.path.exists(sub_directory):
					os.makedirs(sub_directory)
		except OSError as e:
			if e.errno !=17:
				raise
			pass
		return

	def build_url_parameters(self,arguments):
		# if arguments['exact_size']:
		# 	size_array = [x.strip() for x in arguments['exact_size'].split(",")]
		# 	exact_size = ",isz:ex,iszw:" + str(size_array[0]) + ",iszh:" + str(size_array[1])
		# else:
		# 	exact_size = ''

		built_url = "&tbs="
		counter = 0
		params = {'color_type':[arguments['color_type'],{'full-color':'ic:color', 'black-and-white':'ic:gray','transparent':'ic:trans'}],
				  'size':[arguments['size'],{'large':'isz:l','medium':'isz:m','icon':'isz:i','>400*300':'isz:lt,islt:qsvga','>640*480':'isz:lt,islt:vga','>800*600':'isz:lt,islt:svga','>1024*768':'visz:lt,islt:xga','>2MP':'isz:lt,islt:2mp','>4MP':'isz:lt,islt:4mp','>6MP':'isz:lt,islt:6mp','>8MP':'isz:lt,islt:8mp','>10MP':'isz:lt,islt:10mp','>12MP':'isz:lt,islt:12mp','>15MP':'isz:lt,islt:15mp','>20MP':'isz:lt,islt:20mp','>40MP':'isz:lt,islt:40mp','>70MP':'isz:lt,islt:70mp'}],
				  'type':[arguments['type'],{'face':'itp:face','photo':'itp:photo','clipart':'itp:clipart','line-drawing':'itp:lineart','animated':'itp:animated'}],
				  'format':[arguments['format'],{'jpg':'ift:jpg','gif':'ift:gif','png':'ift:png','bmp':'ift:bmp','svg':'ift:svg'}]}
		for key, value in params.items():
			if value[0] is not None:
				ext_param = value[1][value[0]]
				if counter == 0:
					built_url = built_url+ext_param
					counter += 1
				else:
					built_url = built_url + "," + ext_param
					counter += 1
		built_url = built_url
		return built_url

	def build_search_url(self,search_term,params,url,safe_search):
		safe_search_string = "&safe=active"
		if url:
			url = url
		else:
			url = 'https://www.google.com/search?q=' + quote(search_term) + "&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch" + params + "&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg"
		
		if safe_search:
			url = url + safe_search_string

		return url

	def download_page(self,url):
		try:
			headers = {}
			headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
			req = urllib2.Request(url, headers = headers)
			try:
				response = urllib2.urlopen(req)
			except URLError:
				context = ssl._create_unverified_context()
				response = urlopen(req,context = context)
			page = response.read()
			return page
		except:
			print("Could not open URL, Pleae check your internet connection and/or ssl settings")
			return "Page Not found"

	def download_extended_page(self,url,chromedriver):
		from selenium import webdriver
		from selenium.webdriver.common.keys import Keys
		reload(sys)
		sys.setdefaultencoding('utf8')
		options = webdriver.ChromeOptions()
		options.add_argument('--no-sandbox')
		options.add_argument('--headless')

		try:
			browser = webdriver.Chrome(chromedriver, chrome_options = options)
		except Exception as e:
			print("Looks like we cannot locate the path the 'chromedriver' (use the '--chromedriver' "
                  "argument to specify the path to the executable.) or google chrome browser is not "
                  "installed on your machine (exception: %s)" % e)
			sys.exit()
		browser.set_window_size(1024,768)

		browser.get(url)
		time.sleep(1)
		print("Getting you a lot of images, This may take a few moments...")

		element = browser.find_element_by_tag_name("body")

		for i in range(30):
			element.send_keys(Keys.PAGE_DOWN)
			time.sleep(0.3)

		try:
			browser.find_element_by_id("smb").click()
			for i in range(50):
				element.send_keys(Keys.PAGE_DOWN)
				time.sleep(0.3)
		except:
			for i in range(10):
				element.send_keys(Keys.PAGE_DOWN)
				time.sleep(0.3)
		print("Reached end of Page.")
		time.sleep(0.5)

		source = browser.page_source
		browser.close()

		return source

	def replace_with_byte(self,match):
		return chr(int(match.group(0)[1:],8))


	def repair(self,brokenjson):
		invalid_escape = re.compile(r'\\[0-7]{1,3}')
		return invalid_escape.sub(self.replace_with_byte, brokenjson)

	def _get_next_item(self,page):
		start_line = page.find('rg_meta notranslate')
		if start_line == -1:
			end_quote = 0
			link = "no_links"
			return link, end_quote
		else:
			start_line = page.find('class="rg_meta notranslate">')
			start_object = page.find('{', start_line + 1)
			end_object = page.find('</div>', start_object + 1)
			object_raw = str(page[start_object:end_object])

			try:
				final_object = (json.loads(self.repair(object_raw)))
			except:
				final_object = ""
			return final_object, end_object


	def format_object(self, object):
		formatted_object = {}
		formatted_object['image_format'] = object['ity']
		formatted_object['image_height'] = object['oh']
		formatted_object['image_width'] = object['ow']
		formatted_object['image_link'] = object['ou']
		formatted_object['image_description'] = object['pt']
		formatted_object['image_host'] = object['rh']
		formatted_object['image_source'] = object['ru']
		formatted_object['image_thumbnail_url'] = object['tu']
		return formatted_object

	def download_image(self,image_url,image_format,main_directory,dir_name,count,print_urls):
		if print_urls:
			print("Image URL: " + image_url)
		try:
			req = Request(image_url, headers = {"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
			try:
				timeout = 10
				response = urlopen(req,None,timeout)
				data = response.read()
				response.close()

				image_name = str(image_url[(image_url.rfind('/'))+1:])
				image_name = image_name.lower()

				if image_format == "":
					image_name = image_name + "." + "jpg"
				elif image_format == "jpeg":
					image_name = image_name[:image_name.find(image_format)+4]
				else:
					image_name = image_name[:image_name.find(image_format)+3]

				path = main_directory + "/" + dir_name + "/" + str(count) + ". " + image_name

				try:
					output_file = open(path,'wb')
					output_file.write(data)
					output_file.close()
					absolute_path = os.path.abspath(path)
				except OSError as e:
					download_status = 'fail'
					download_message = "OSError on an image...trying next one..." + " Error: " + str(e)
					return_image_name = ""
					absolute_path = ""
				
				download_status = "success"
				download_message = "Completed Image ===> "+str(count)+". "+image_name
				return_image_name = str(count) + ". " + image_name

			except UnicodeEncodeError as e:
				download_status = 'fail'
				download_message = "UnicodeEncodeError on an image...trying next one..." + " Error: " + str(e)
				return_image_name = ""
				absolute_path = ""

			except URLError as e:
				download_status = "fail"
				download_message = "URLError on an image...trying next one..." + " Error: " + str(e)
				return_image_name = ""
				absolute_path = ""

		except HTTPError as e:
			download_status = 'fail'
			download_message = "HTTPError on an image...trying next one..." + " Error: " + str(e)
			return_image_name = ""
			absolute_path = ""
		except URLError as e:
			download_status = 'fail'
			download_message = "URLError on an image...trying next one..." + " Error: " + str(e)
			return_image_name = ''
			absolute_path = ''
		except ssl.CertificateError as e:
			download_status = 'fail'
			download_message = "CertificateError on an image...trying next one..." + " Error: " + str(e)
			return_image_name = ''
			absolute_path = ''
		except IOError as e:  # If there is any IOError
			download_status = 'fail'
			download_message = "IOError on an image...trying next one..." + " Error: " + str(e)
			return_image_name = ''
			absolute_path = ''
		except IncompleteRead as e:
			download_status = 'fail'
			download_message = "IncompleteReadError on an image...trying next one..." + " Error: " + str(e)
			return_image_name = ''
			absolute_path = ''

		return download_status,download_message,return_image_name,absolute_path


	def _get_all_items(self,page,main_directory,dir_name,limit,arguments):
		items = []
		abs_path = []
		errorCount = 0
		i = 0
		count = 1
		while count < limit+1:
			object, end_content = self._get_next_item(page)
			if object == "no_links":
				print("No links")
				break
			elif object == "":
				page = page[end_content:]
			else:
				object = self.format_object(object)

				download_status, download_message,return_image_name,absolute_path = self.download_image(object['image_link'],object['image_format'],main_directory,dir_name,count,arguments['print_urls'])
				print(download_message)
				if download_status == "success":
					count += 1
					object['images_filename'] = return_image_name
					items.append(object)
					abs_path.append(absolute_path)
				else:
					errorCount += 1

				page = page[end_content:]
			i += 1
		if count < limit:
			print("\n\nUnfortunately all " + str(
                limit) + " could not be downloaded because some images were not downloadable. " + str(
                count-1) + " is all we got for this search filter!")
		return items, errorCount,abs_path


	def download(self, arguments):
		if arguments['keywords']:
			search_keyword = [str(item) for item in arguments['keywords'].split(',')]
		
		if arguments["limit"]:
			limit = int(arguments["limit"])
		else:
			limit = 100

		if arguments['url']:
			current_time = str(datetime.datetime.now()).split(".")[0]
			search_keyword = [current_time.replace(":", "_")]

		if arguments['output_directory']:
			main_directory = arguments['output_directory']
		else:
			main_directory = "downloads"

		paths = {}
		i = 0
		while i < len(search_keyword):
			iteration = "\n"+"Item no.: " + str(i+1) + "-->" + "Item name = " + str(search_keyword[i])
			print(iteration)
			print("Evaluating...")
			search_term = search_keyword[i]

			if arguments['image_directory']:
				dir_name = arguments['image_directory']
			else:
				dir_name = search_term 

			self.creat_directories(main_directory,dir_name)

			params = self.build_url_parameters(arguments)

			url = self.build_search_url(search_term,params,arguments['url'],arguments['safe_search'])
			print(url)
			if limit < 101:
				raw_html = self.download_page(url)
			else:
				raw_html = self.download_extended_page(url,arguments['chromedriver'])

			print("Starting Download...")
			items,errorCount,abs_path = self._get_all_items(raw_html,main_directory,dir_name,limit,arguments)
			paths[search_keyword[i]] = abs_path

			i += 1
			print("\nErrors: " + str(errorCount) + "\n")
		# if arguments['print_paths']:
		# 	print(paths)
		return paths


def main():
	records = user_input()
	for arguments in records:
		t0 = time.time()
		response = googleimagesdownload()
		paths = response.download(arguments)
		print("\nEverything downloaded")
		t1 = time.time()
		total_time = t1-t0
		print("Total time taken: " + str(total_time) + "Seconds")

if __name__ == "__main__":
	main()
