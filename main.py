
####################################################################################################################
# Import modules
####################################################################################################################

try:

    # General imports
    import os
    import sys
    from datetime import datetime
    import pytz
    from pathlib import Path

    # Import local modules
    sys.path.append('utils')
    from utils.get_secrets import open_secret
    from utils.modify_data import update_gsheet
    from utils.read_data import get_query

except Exception as e:
    raise Exception("Something went wrong importing packages!")


####################################################################################################################
# Set up
####################################################################################################################

# Define paths
PATH_QUERIES = Path('queries')


####################################################################################################################
# Get credentials
####################################################################################################################

try:

    # If the environment variable for the credentials exists, it means that we are running the script locally
    if os.environ.get('CREDENTIALS') is not None:
        path_credentials = os.environ['CREDENTIALS']
        #print('\nUsing local credentials')
        jenkins = False

    # Otherwise, we are not in our local machine, but in Jenkins
    else:
        path_credentials = "foo"
        #print('\nUsing Jenkins secrets')
        jenkins = True

    # Define paths for credentials
    path_sheets = os.path.join(path_credentials, 'gsheets_credentials.json')
    path_dwh = os.path.join(path_credentials, 'dwh_credentials.json')
    path_liveDB = os.path.join(path_credentials, 'liveDB_credentials.json')

    # Open credentials
    credentials_DWH = open_secret(path_dwh, 'supply_growth_dwh')
    credentials_liveDB = open_secret(path_liveDB, 'supply_growth_liveDB')

except Exception as e:
    raise Exception('Something went wrong when reading the credentials')


####################################################################################################################
# Helper functions
####################################################################################################################

def update_tab(spreadhseet_id, path_to_queries, sql_file, position, sheet_tab):

    try:
        #print(f"\nUpdating tab {sheet_tab} with SQL file '{sql_file}'")
        df_raw = get_query(path_to_queries, sql_file, credentials_liveDB, database='liveDB')
        update_gsheet(spreadhseet_id, sheet_tab, df_raw, path_sheets, position, jenkins)

    except Exception as e:
        raise Exception("Something went wrong for query {}".format(sql_file))


####################################################################################################################
# Main
####################################################################################################################

if __name__ == "__main__":


    ####################################################################################################################
    # Challenges query
    ####################################################################################################################

    # Define Google Sheet ID to paste the metrics
    sheet_id = '16nW27L4yqAnDMN3xqUHiL1tFcn7UxbaK3fE7d-2vQo4'

    update_tab(sheet_id, PATH_QUERIES, sql_file='Challenges.sql', position='First_row', sheet_tab='live_data')