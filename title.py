import requests
import sys
from tempfile import NamedTemporaryFile
from json import loads
import NetflixRoulette as nf
from xml.etree import ElementTree as ET
if __name__ == '__main__':
    def _main():
        itemsRoot = ET.Element('items')
        data = nf.get_all_data(sys.argv[1])
        if 'error_code' in data:
            message = data['message']
            item = ET.SubElement(itemsRoot, 'item')
            item.attrib = {
                'arg': 'clean',
                'uid': '0',
                'valid': 'no'
            }
            title = ET.SubElement(item, 'title')
            title.text = message
            subtitle = ET.SubElement(item, 'subtitle')
            subtitle.text = data['error_code']

        else:
            item = ET.SubElement(itemsRoot, 'item')
            item.attrib = {
                'arg': 'clean',
                'uid': '0',
                'valid': 'yes'
            }
            title = ET.SubElement(item, 'title')
            title.text = data['show_title']
            res = requests.get(data['poster'], stream=True)
            fi = NamedTemporaryFile(delete=False)
            path = fi.name
            with fi as f:
                for chunk in res.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()
            icon = ET.SubElement(item, 'icon')
            icon.text = path
            subtitle = ET.SubElement(item, 'subtitle')
            subtitle.text = data['summary']
            rating = data['rating']
        sys.stdout.write(ET.tostring(itemsRoot))
            
    _main()
