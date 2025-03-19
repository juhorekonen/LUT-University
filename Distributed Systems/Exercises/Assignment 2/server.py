# Server-side for an RPC system
import os
import xml.etree.ElementTree as ET
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import requests

FILE = 'data.xml'
WIKI_URL = 'https://en.wikipedia.org/api/rest_v1/page/summary/'

def initialize():
    if not os.path.exists(FILE):
        root = ET.Element('data')
        tree = ET.ElementTree(root)
        # Try to create the file if not exists
        try:
            tree.write(FILE)
        except Exception as e:
            print('Error occurred while creating an XML file: {e}')
            return  

# Function to add a note to a topic
def addNote(topic, text, timestamp):
    try:
        tree = ET.parse(FILE)
        root = tree.getroot()

        topicElement = None
        for note in root.findall('topic'):
            if note.get('name') == topic:
                topicElement = note
                break
        if topicElement is None:
            topicElement = ET.SubElement(root, 'topic')
            topicElement.set('name', topic)
        
        noteElement = ET.SubElement(topicElement, 'note')
        textElement = ET.SubElement(noteElement, 'text')
        textElement.text = text
        timestampElement = ET.SubElement(noteElement, 'timestamp')
        timestampElement.text = timestamp
        tree.write(FILE)
    except Exception as e:
        print('Error occurred while adding a note: {e}')
        return 'Error occurred while adding a note'
    
    return f"Note added to topic {topic}"

# Function to retrieve notes for a topic
def getNotes(topic):
    try:
        tree = ET.parse(FILE)
        root = tree.getroot()
        notes = []

        for t in root.findall('topic'):
            if t.get('name') == topic:
                for n in t.findall('note'):
                    text = n.find('text').text
                    timestamp = n.find('timestamp').text
                    notes.append((text, timestamp))

        if notes == []:
            return 'No notes found for topic ' + topic
    except Exception as e:
        print('Error occurred while retrieving notes: {e}')
        return 'Error occurred while retrieving notes'
    
    return notes

# Function to fetch a topic from Wikipedia
def fetchWikipedia(topic):
    try:
        response = requests.get(WIKI_URL + topic)
        if response.status_code != 200:
            return 'Error occurred while fetching topics from Wikipedia'
        
        data = response.json()
        summary = data.get('extract', 'No summary available')
        text = f'Wikipedia Summary: {summary}'
        return addNote(topic, text, 'Wikipedia')
    except Exception as e:
        print('Error occurred while fetching topics from Wikipedia: {e}')
        return 'Error occurred while fetching topics from Wikipedia'

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

initialize()

server = SimpleXMLRPCServer(('localhost', 8000), requestHandler=RequestHandler, allow_none=True)
server.register_function(addNote, 'addNote')
server.register_function(getNotes, 'getNotes')
server.register_function(fetchWikipedia, 'fetchWikipedia')

print('Server running on port 8000')
server.serve_forever()