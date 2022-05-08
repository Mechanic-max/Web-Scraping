from helper_class import *
from interface_class import *

class MAINCLASS():

	def __init__(self):
		self.helper = Helper()
		self.config = self.helper.read_json_file('./config.json')

		driver_type = self.config['driver_type']
		# headless_browser =self.config['start_maximized']
		driver_path = self.config['chrome_driver_path']
		self.interface = INTERFACING(driver_type,driver_path)

		self.main_url = self.config['main_url']
		self.data_folder = self.helper.checking_folder_existence(self.config['output_data_folder'])
		self.log_folder = self.helper.checking_folder_existence(self.data_folder + self.config['output_log_folder'])

		self.headers = []
		self.is_initialized = False

	def writing_output_file(self,sub_list):

		output_file = self.data_folder + 'cuyahoga_county_complete.csv'

		if self.helper.is_file_exist(output_file):
			input_data = self.helper.reading_csv(output_file)
		else:
			input_data =[]
			input_data.append(self.headers)

		input_data.append(sub_list)
		self.helper.writing_csv(input_data,output_file)
		print("Writing Output File Done...")

	def get_response(self,link):
		soup = False
		while not soup:
			soup = self.interface.get_selenium_response(link)
			time.sleep(2)
		#print("Response from Link: ", link, " is poisitve. moving Forward....")

		return soup

	def processing_each_parcel_number(self,current_parcel_number,_input_data):

		soup = self.get_response(self.main_url)

		addr = '//input[@id="Address"]'
		self.interface.clicking(addr)
		
		parcel_xpath = '//*[@id="txtData"]'
		self.interface.entering_values(parcel_xpath,current_parcel_number)

		search_button_xpath = '//*[@id="btnSearch"]'
		self.interface.clicking(search_button_xpath)
		try:
			summary_report_xpath = '//*[@id="btnPropertyCardInfo"]'
			self.interface.clicking(summary_report_xpath)
		except:
			print("There is nothing to scrap")
		

		soup = self.interface.make_soup()

		if soup.find('table',class_='PropertyCardGeneralTable') is None:
			print("No Data Available")
			self.writing_output_file(_input_data)
			return

		owner_name = soup.find('td',text='Owner').find_next_sibling('td').get_text().strip()

		mailing_address_html = []
		mailing_address_html.append(soup.find('td',text='Address').find_next_sibling('td').get_text().strip())

		next_sibling = soup.find('td',text='Address').find_next_sibling('td').parent.find_next_sibling('tr')
		mailing_address_html.append(next_sibling.find_all('td')[1].get_text().strip())

		next_sibling = next_sibling.find_next_sibling('tr')
		if len(next_sibling.td.get_text().strip()) < 1:
			mailing_address_html.append(soup.find('td',text='Address').find_next_sibling('td').get_text().strip())

		mailing_address = ' '.join(mailing_address_html[:-1])
		mailing_city = mailing_address_html[-1].split(',')[0]
		mailing_state = mailing_address_html[-1].split(',')[1].split('.')[0]
		mailing_zip = mailing_address_html[-1].split(',')[1].split('.')[1]

		property_address_html = soup.find('span',text='Property Summary Report').find_next_sibling('ul').find_all('li')
		property_address_1 = []

		for prop in property_address_html:
			if len(prop.get_text().strip()) > 0:
				property_address_1.append(prop.get_text().strip())

		owner_index = property_address_1.index(owner_name)
		site_address = ' '.join(property_address_1[owner_index+1:-1])
		site_city = property_address_1[-1].split(',')[0]
		site_state = property_address_1[-1].split(',')[1].split('.')[0]
		site_zip = property_address_1[-1].split(',')[1].split('.')[1]

		property_type = soup.find('td',text='Land Use').find_next_sibling('td').get_text().strip()

		print("Owner Name: ", owner_name)
		print("Mailing Address: ", mailing_address)
		print("Mailing City: ", mailing_city)
		print("Mailing State: ", mailing_state)
		print("Mailing Zip: ", mailing_zip)
		print("Site Address: ", site_address)
		print("Site City: ", site_city)
		print("Site State: ", site_state)
		print("Site Zip: ", site_zip)
		print("Property Type: ",property_type)

		if soup.find('td',text='Year Built') is not None:
			year_built = soup.find('td',text='Year Built').find_next_sibling('td').get_text().strip()
		else:
			year_built = ''

		if soup.find('td',text='Bathrooms') is not None:
			baths = soup.find('td',text='Bathrooms').find_next_sibling('td').get_text().strip()
		else:
			baths = ''

		if soup.find('td',text='Bedrooms') is not None:
			beds = soup.find('td',text='Bedrooms').find_next_sibling('td').get_text().strip()
		else:
			beds = ''

		if soup.find('td',text='Living Area Total') is not None:
			living_area = soup.find('td',text='Living Area Total').find_next_sibling('td').get_text().strip()
		else:
			living_area = ''

		land_value = soup.find('td',text='Land Value').find_next_sibling('td').get_text().strip()
		bldg_value = soup.find('td',text='Building Value').find_next_sibling('td').get_text().strip()
		total_assessed_value = soup.find('td',text='Total Value').find_next_sibling('td').get_text().strip()
		print("Land Value: ", land_value)
		print("Building Value: ", bldg_value)
		print("Total Assessed Value: ", total_assessed_value)

		try:
			sales_latest_date = soup.find('table',class_='PropertyCardSalesTable').find_all('tr')[1].td.get_text().strip()
		except:
			sales_latest_date = ''
		try:
			sales_latest_amount = soup.find('table',class_='PropertyCardSalesTable').find_all('tr')[1].find_all('td')[-1].get_text().strip()
		except:
			sales_latest_amount = ''
		print("Latest Sales Date: ", sales_latest_date)
		print("Latest Sales Amount: ", sales_latest_amount)

		_input_data.extend([current_parcel_number,owner_name,mailing_address,mailing_city,mailing_state,mailing_zip])
		_input_data.extend([site_address,site_city,site_state,site_zip,year_built,property_type,living_area,baths,beds])
		_input_data.extend([land_value,bldg_value,total_assessed_value,sales_latest_date,sales_latest_amount])

		self.writing_output_file(_input_data)

	def start_dynamic_scraping(self):

		input_data_file = './input_data/input_data_file.csv'
		input_data = self.helper.reading_csv(input_data_file)
		processed_json_file = self.log_folder + 'processed.json'
		processed_json_data = self.helper.json_exist_data(processed_json_file)

		self.headers.extend(input_data[0])
		self.headers.extend(["parcel_number", "owner_name", "mailing_address", "mailing_city", 
							"mailing_state", "mailing_zip", "site_address", "site_city", "site_state",
							"site_zip", "year_built", "property_type", "living_area", "baths", "bedrooms",
							"land_value","bldg_value", "total_assessed_value", 
							"sales_latest_date","sales_latest_amount"])

		starting_index = 1
		ending_index = len(input_data)

		for data in range(starting_index,ending_index):

			current_parcel_number = input_data[data][0]

			print(data , " / ", ending_index," : ------Current Processing: ", current_parcel_number)
			if current_parcel_number not in processed_json_data:
				self.processing_each_parcel_number(current_parcel_number,input_data[data])
				processed_json_data.append(current_parcel_number)
				self.helper.write_json_file(processed_json_data,processed_json_file)
			else:
				print("Already Processed")
				print()

			print('*'*50)
			print()
		self.interface.close_driver()


if __name__ == "__main__":
	handle = MAINCLASS()
	handle.start_dynamic_scraping()
	
