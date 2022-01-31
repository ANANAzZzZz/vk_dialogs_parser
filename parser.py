from bs4 import BeautifulSoup
import emoji
import os


def get_text_dialogs():

    print('Input link on directory with html data from vk dialogs: ')
    print('(Directory should be inside project)')
    eternal_link = input()

    # get names of all html documents from directory
    all_data = os.listdir(eternal_link)

    number_of_html = 0
    for element in all_data:
        link = eternal_link + element
        get_messages(link)

        print('parsing html № ', number_of_html)
        number_of_html += 1


def get_messages(link):
    data = open(link, "r")
    html = data.read()

    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('div', class_='item')

    parse_html_items(items)


def parse_html_items(items):
    # open output file
    output = open('dialogs.txt', 'a')

    # counter for spliting dialogs on logic blocks
    counter = 0

    for item in reversed(items):
        # searching tag message inside tag item
        message = item.find('div', class_='message')

        try:
            # if message is attachment decompose it
            item = item.find('div', class_='attachment').decompose()
            message = None
        except:
            pass

        if message is not None:
            # if message is text start parsing
            message.div.decompose()
            message = message.get_text().strip()

            try:
                # check the message on emoji
                if ":" not in emoji.demojize(message):
                    # if it is not an emoji, write message to the output
                    output.write(chr(10))
                    output.write('- ' + message)

                    # add logical indents
                    if counter % 2 == 0:
                        output.write(chr(10))
                    counter += 1
            except:
                pass

get_text_dialogs()

print()
print('Data parsed succesfuly \n'
      'check it out inside project directory')
