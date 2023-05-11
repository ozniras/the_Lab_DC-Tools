from boxsdk import OAuth2, Client
import json
import os

def update_credentials(credentials_file='', access_token='', client_secret='', client_id=''):
    
    # Check for minimum requisites
    if credentials_file == '':
        print('ERROR: Need a filename.')
        return
    if access_token == '':
        print('ERROR: Need an access token to update (or create a new credentials file)')
        return
    
    # If the file exists
    if os.path.isfile(credentials_file):
        # Check that file has the proper structure
        try:
            with open(credentials_file) as json_file:
                data = json.load(json_file)
                
        except:
            print('ERROR: While reading credentials file.')
            return
                
        # Check that file has the required fields
        if ('client_id' not in data) & (client_id == ''):
            print('ERROR: No client id in file and none provided')
            return
        if ('client_secret' not in data) & (client_secret == ''):
            print('ERROR: No client secret in file and none provided')
            return
        
    # If file does not exist, make sure we have all necessary inputs
    else:
        # Check that the required fields were passed
        if client_id == '':
            print('ERROR: No client id provided')
            return
        if client_secret == '':
            print('ERROR: No client secret in provided')
            return
        
        data = {}
        data['client_id'] = client_id
        data['client_secret'] = client_secret
        
    # pass new developer token
    data['access_token'] = access_token
    
    #Output new file
    with open(credentials_file, 'w') as outfile:
        json.dump(data, outfile)
            
    return None
        

def start_box_connection(credentials_file=''):
    '''Starts a connection to Box using box sdk.
    Opens a json file (simple dictionary) to read:
    - client_id
    - client_secret
    - access_token (aka developer token)
    Inputs:
    - Path to json file with developer info
    Outputs:
    - client connection
    Note: the current version does NOT check for the existence of this file, you must create it.
    '''
    with open(credentials_file) as json_file:
        data = json.load(json_file)
        auth = OAuth2(
        client_id=data['client_id'],
        client_secret=data['client_secret'],
        access_token=data['access_token']
        )
    
    return Client(auth)
    

def download_box_file(client=None, file_id='', destination=''):
    '''Downloads a box file and saves it locally
    Inputs:
    - client: client connection (create using start_box_connection())
    - file_id: string with the file id
    - destination: path AND NAME for where you want the file saved
    Outputs:
    - You should see the file saved in destination
    Note: the current version does NOT check for errors'''
    with open(destination, 'wb') as output_file:
        client.file(file_id).download_to(output_file)
    return None

def upload_box_file(client=None, folder_id=None, file_name=''):
    '''Uploads a file into a box folder
    Inputs:
    - client: client connection (create using start_box_connection())
    - folder_id: string with the destination folder id
    - file_name: name (with local path) of the file you want to upload
    Outputs:
    - You should see the file uploaded to the box account 
    '''
    new_file = client.folder(folder_id).upload(file_name)
    return None

    
client = start_box_connection(credentials_file='./credentials.json')
download_box_file(client=client, file_id='942204689174', destination='./local2.docx')
upload_box_file(client=client, folder_id='132850993426', file_name='./local.docx')