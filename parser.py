from bs4 import BeautifulSoup
import emoji
import os
import sys


class Counter:

    def __init__(self):
        self._value = 0


    def new_value(self):
        self._value += 1
        return self._value


    def print_value(self):
        return self._value


def get_text_dialogs():
    print('Input link on directory with html data from vk dialogs: ')
    print('(Directory should be inside project)')
    eternal_link = input()

    try:
        # get names of all html documents from directory
        all_data = os.listdir(eternal_link)

        # counters
        number_of_html = Counter()

        for element in all_data:
            # generating link to the element
            link = eternal_link + element

            get_messages(link)

            print('parsing html № ', number_of_html.print_value())
            number_of_html.new_value()

        output_info()

    except FileNotFoundError:
        print('Enter correct adress')

        sys.exit()

    except KeyboardInterrupt:
        print('Scipt has been interrupted')

        sys.exit()


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
    split = Counter()

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
                    if split.print_value() % 2 == 0:
                        output.write(chr(10))
                    split.new_value()

            except:
                pass


def output_info():
    print('\nData parsed succesfuly \n'
        'Check it out inside project directory \n')


get_text_dialogs()
