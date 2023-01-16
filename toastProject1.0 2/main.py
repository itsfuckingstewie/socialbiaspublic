from random import uniform as random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from time import sleep
from time import time
from fake_useragent import UserAgent as useragent
from webdriver_manager.chrome import ChromeDriverManager

def antiban_browser_restart():
    print('Antiban browser restart.')
    start_time_antiban = time()
    browser.quit()
    browser_init()
    print('Done in {} seconds.'.format(str((time()-start_time_antiban))[:4]))

def antiban_sleep():
    global sleep_length
    print('Antiban sleep for {} seconds.'.format(sleep_length))
    sleep(sleep_length)
    print()

def browser_init():
    options = Options()
    global headless
    if headless: options.add_argument('--headless') #disables gui
    #options.add_argument('start-maximized')
    #options.add_argument('--disable-extensions')
    options.add_argument('--window-size=1080,720');
    options.add_argument('enable-features=NetworkServiceInProcess');
    options.add_argument('disable-features=NetworkService');
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-browser-side-navigation')
    options.add_argument('--force-device-scale-factor=1')
    options.add_argument('--log-level=3') #disables extensive log
    #options.add_argument('enable-automation') maybe redundant, better off for masking
    if captcha_auto_solving: options.add_argument('--load-extension=C:/Users/jajce3/Desktop/active/code/toastProjectGoogleCorpiCross/nopecha') #install captcha buster extension

    #antiban: potential webdriver masking
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--disable-blink-features')
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    global browser
    browser = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = options)

    #antiban: potential webdriver masking
    browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    #antiban: mask user agent
    if fallback_user_agent: user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    else:
        user_agent = useragent().random
    browser.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent})

def search(search_string):
    url = 'https://www.google.com/search?q="{}"'.format(search_string)
    browser.get(url)
    try: return int(browser.find_element('id', 'result-stats').text.split(' ')[1].replace('.', ''))
    except:
        print()
        if captcha_auto_solving:
            print('Solving CAPTCHA.. (or there is an error)')
            sleep(captcha_solving_delay)
        else:
            input('Solve CAPTCHA, then hit enter to continue.')
        print()
        return search(search_string)
    
def main():
    print('Loading browser.')
    start_time = time()
    browser_init()
    print('Done in {} seconds.'.format(str((time()-start_time))[:4]))
    sleep(0.5)
    print()

    filename = str(input('Enter filename or hit enter for default.\n'))
    if filename == '':
        filename = default_filename
        print('Default: {}'.format(default_filename))
    print()
    sleep(0.5)

    print('Searching.')
    print()
    global start_time_search
    start_time_search = time()
    
    with open('lists/'+filename) as search_list:
        counter = 0
        for search_string in search_list:
            if search_string[0] == '#': continue
            
            counter += 1
            if start_line > counter: continue
            
            search_string = search_string.replace('\n', '')
            
            if counter % (antiban_trigger + 1) == 0:
                print()
                print('Running for {} seconds.'.format(int(time()-start_time_search)))
                sleep(0.5)
                antiban_browser_restart()
                sleep(0.5)
                antiban_sleep()

            sleep(random(antiban_search_delay[0],antiban_search_delay[1])) 
            occurrence = search(search_string.split(' ')[0])
            
            print(' '*(5-len(str(counter)))+str(counter), ' '*(20-len(search_string))+search_string, ' '*(11-len(str(occurrence)))+str(occurrence))
            if write_to_file:
                with open('output/'+filename, 'a') as output_file:
                    output_file.write(search_string+' '+str(occurrence)+'\n')
            
    print('Searching took {} seconds.'.format(str((time()-start_time_search))[:4]))
    print()

    browser.quit()
    print('END')

global antiban_search_delay
global antiban_trigger
global default_filename
global headless
global sleep_length
global start_line
global write_to_file
antiban_search_delay = (0, 0) #(0.3, 2.5)
antiban_trigger = 64
captcha_auto_solving = 0
captcha_solving_delay = 15
default_filename = 'wiki-100k.txt'
fallback_user_agent = 1
headless = 0
sleep_length = 120
start_line = 0
write_to_file = 1

main()
