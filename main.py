import os, pygame, time, datetime, settings, random
from urllib2 import urlopen, URLError, HTTPError
def main():
    previous_date = None
    current_date = None
    running = True
    while running:
        current_date = datetime.date.today()
        if current_date != previous_date:
            refresh_files()
        previous_date = current_date
        random_picture = random.choice(os.listdir(settings.DOWNLOAD_LOCATION))
        display_picture('images/' + random_picture)
        time.sleep(settings.IMAGE_TIMEOUT)
        running = handle_events()
    pygame.quit()
    
def refresh_files():
    delete_files(settings.DOWNLOAD_LOCATION)
    urls = get_file_list()
    for i in range(0, len(urls)):
        download_files(urls[i])
        
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
    return True

def display_picture(source):
    picture = pygame.image.load(source)
    picture = pygame.transform.scale(picture,(settings.RESOLUTION_WIDTH,settings.RESOLUTION_HEIGHT))
    pygame.display.set_mode((settings.RESOLUTION_WIDTH,settings.RESOLUTION_HEIGHT),pygame.FULLSCREEN)
    main_surface = pygame.display.get_surface()
    main_surface.blit(picture, (0, 0))
    pygame.display.update()
    pygame.mouse.set_visible(0)
    
def get_file_list():
    endpoint = settings.PHOTO_ENDPOINT
    #endpoint = settings.PHOTO_ENDPOINT_TEST
    response = urlopen(endpoint + settings.NUM_NEW_PHOTOS)
    html = response.read()
    return html.split(',')

def delete_files(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        os.unlink(file_path)

def download_files(url):
    try:
        f = urlopen(url)
        filesave_location = settings.DOWNLOAD_LOCATION + os.path.basename(url)
        if not os.path.isfile(filesave_location):
            with open(filesave_location, "wb") as local_file:
                local_file.write(f.read())

    #handle errors
    except HTTPError, e:
        print "HTTP Error:", e.code, url
    except URLError, e:
        print "URL Error:", e.reason, url

if  __name__ =='__main__':main()
