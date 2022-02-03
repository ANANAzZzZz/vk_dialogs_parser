import emoji
import os
import sys

from bs4 import BeautifulSoup
from classes.Counter import Counter


def get_text_dialogs():
    print('Input link on directory with html data from vk dialogs: ')
    print('(Directory should be inside project)')
    eternal_link = input()

    try:
        # get names of all html documents from directory
        all_data = os.listdir(eternal_link)

        # counters
        messages_counter = Counter()
        attachment_counter = Counter()
        number_of_html = Counter()
        demojize_failed = Counter()

        for element in all_data:
            # generating link to the element
            link = eternal_link + element

            get_messages(link, messages_counter, attachment_counter, demojize_failed)

            print('parsing html № ', number_of_html.get_value() + 1)
            number_of_html.new_value()

        output_info(messages_counter, attachment_counter, demojize_failed)


    except FileNotFoundError:
        print('Enter correct adress')

        sys.exit()


    except KeyboardInterrupt:
        print('Scipt has been interrupted')

        sys.exit()


def get_messages(link, messages_counter, attachment_counter, demojize_failed):
    # open html file using link
    data = open(link, "r")
    html = data.read()

    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('div', class_='item')

    messages_counter = parse_html_items(items, messages_counter, attachment_counter, demojize_failed)

    return messages_counter, attachment_counter, demojize_failed


def parse_html_items(items, messages_counter, attachment_counter, demojize_failed):
    # open output file
    output = open('dialogs.txt', 'a')

    # counter for spliting dialogs on logic blocks
    split_counter = Counter()

    for item in reversed(items):
        # searching tag message inside tag item
        message = item.find('div', class_='message')

        try:
            # if message is attachment decompose it
            item = item.find('div', class_='attachment').decompose()
            message = None

            attachment_counter.new_value()

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

                    # increase message counter
                    messages_counter.new_value()

                    # add logical indents
                    if split_counter.get_value() % 2 == 0:
                        output.write(chr(10))
                    split_counter.new_value()

            except:
                demojize_failed.new_value()

    return messages_counter, attachment_counter, demojize_failed


def output_info(message_counter, attachment_counter, demojize_failed):
    print('\nData parsed succesfuly \n'
        'Check it out inside project directory \n'
        f'\nParsed {message_counter.get_value()} messages'
        f'\nRemoved {attachment_counter.get_value()} attachments \n'
        '\nErrors:'
        f'\nDemojize_failed: {demojize_failed.get_value()}')


get_text_dialogs()