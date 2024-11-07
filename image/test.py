from gdrive import writeFile


def handler(event, context):

    writeFile()
    
if __name__ == '__main__':
    handler(None, None)