import requests
from bs4 import BeautifulSoup
from datetime import datetime
import concurrent.futures
import time
import csv

# Function to check if an ID already exists in the CSV file
def id_exists(id, filename):
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        for row in reader:
            if row[0] == id:
                return True
    return False

def convert_date(date_string):
    # Add default year as 2023 if the year is missing
    if len(date_string.split()) < 3:
        date_string += ' 2023'

    # Convert the date string to a datetime object
    try:
        date = datetime.strptime(date_string, '%d %b %Y')
    except ValueError:
        date = datetime.strptime(date_string, '%B %d %Y')

    # Format the date as DD/MM/YYYY
    formatted_date = date.strftime('%d/%m/%Y')

    return formatted_date

def write_comment_csv(comment_list, id):
    with open('./comments/' + id +'_comments.csv', 'w', encoding='utf-8') as f:
        f.write('Date,Name,Comment\n')
        for item in comment_list:
            f.write(item + '\n')

def get_idea_links(page):
    r = requests.get(page)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        for item in soup.find_all('a', class_='idea-link'):
            yield item.get('href')
    else:
        raise Exception('Error')

def scrape_idea_page(page):
    
    id = page.split('/')[-1].replace(',', '')

    max_retries = 3
    retry_delay = 2

    for _ in range(max_retries):
        try:
            r = requests.get(page)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                name = soup.find('h2').text.strip().replace(',', '')
                votes = soup.find('span', class_='vote-count').text.strip().replace(',', '')
                description_div = soup.find('div', class_='description').find_all('p')
                description = ''

                for item in description_div:
                    description = description + ' ' + item.text.strip().replace(',', '').replace('\n', '')

                meta = soup.find('ul', class_='idea-meta').text.strip()
                date = meta.split('\n')[3].strip().replace(',', '')
                status = meta.split('\n')[-1].strip().replace(',', '')

                if status == date:
                    status = 'None'

                date = datetime.strptime(date, '%b %d %Y').strftime('%d/%m/%Y')

                comment_div = soup.find_all('div', class_='body')
                
                # Create CSV of Comments
                comment_list = []
                
                for item in comment_div:
                    comment_date = item.text.split('\n')[9][:-6].strip().replace(',', '')
                    comment_name = item.text.split('\n')[4][:-10].strip().replace(',', '')
                    comment_date = convert_date(comment_date)
                    
                    if item.find('p') is not None:
                        comment_text = item.find('p').text.strip().replace(',', '').replace('\n', ' ')
                    else:
                        comment_text = ''
                    comment_list.append(comment_date + ',' + comment_name + ',' + comment_text)
                
                write_comment_csv(comment_list, id)
                        

                return id + ',' + name + ',' + votes + ',' + description.lstrip() + ',' + date + ',' + status + ',' + page

            else:
                print('Error: Could not retrieve page - ' + page)
                return None
        except requests.exceptions.RequestException:
            pass

        time.sleep(retry_delay)

    raise Exception('Error: Failed to retrieve page')

def scrape_ideas_page(page):
    ideas = []
    for link in get_idea_links(page):
        ideas.append('https://wishlist.webflow.com' + link)
    return ideas

def main():
    url = 'https://wishlist.webflow.com/?page={}'
    ideas = []
    scraped = []
    count = 1

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Gather links using multiple threads
        for i in range(1, 310):
            page = url.format(i)
            print('Gathering links on page ' + str(i))
            future = executor.submit(scrape_ideas_page, page)
            ideas.extend(future.result())

        # Scrape idea details using multiple threads
        for idea in ideas:
            print('Scraping URL #' + str(count) + ': ' + idea)
            count += 1
            future = executor.submit(scrape_idea_page, idea)
            result = future.result()
            if result is not None:
                scraped.append(result)
    
    # Check and append scraped data to the existing CSV file
    existing_data = set()
    with open('output.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        for row in reader:
            existing_data.add(row[0])  # Store IDs in a set

    with open('output.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for item in scraped:
            id = item.split(',')[0]
            if id not in existing_data and not id_exists(id, 'output.csv'):
                writer.writerow(item.split(','))

if __name__ == '__main__':
    main()