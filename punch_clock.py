#!/usr/bin/env python3

import gspread, json, math, os, sys

from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials

# Temporary way to load the sheet's key
import sheet_key

scope = ['https://spreadsheets.google.com/feeds'];

dir_path = os.path.dirname(os.path.realpath(__file__));
creds_file_path = os.path.join(dir_path, 'creds.json');

# Authorize and initialize gspread client
credentials = ServiceAccountCredentials.from_json_keyfile_name(creds_file_path, scope);
client = gspread.authorize(credentials);

# Open the document
doc = client.open_by_key(sheet_key.key);


def get_current_sheet():
    now = datetime.now();
    sheetname = '{} {}'.format(now.strftime('%b'), now.year);

    return doc.worksheet(sheetname);

def round_to_nearest_quarter(date_time):
    Y = date_time.year;
    M = date_time.month;
    D = date_time.day;
    H = date_time.hour;
    m = int(round(date_time.minute / 15.0) * 15);

    # Handle the special case when rounding up to the hour
    if(m == 60):
        m = 0;
        H += 1;

    return datetime(Y, M, D, H, m, 0);

def punch_in_out(action):
    punch_time = datetime.now();
    print(action, punch_time);

    date_str = '{}. {}'.format(punch_time.day, punch_time.strftime('%b'));

    sheet = get_current_sheet();
    date_cell = sheet.find(date_str);

    timestamp_str = round_to_nearest_quarter(punch_time).strftime('%X');

    if(action == 'SCREEN_UNLOCKED'):
        target_cell = sheet.cell(date_cell.row, date_cell.col+1);

        # Only punch in if there is no previous punch that day
        if(target_cell.input_value is ''):
            sheet.update_cell(target_cell.row, target_cell.col, timestamp_str);

    elif(action == 'SCREEN_LOCKED'):
        target_cell = sheet.cell(date_cell.row, date_cell.col+2);

        if(target_cell.input_value is ''):
            sheet.update_cell(target_cell.row, target_cell.col, timestamp_str);
        else:
            # It shouldn't really happen that we're punching in again with a time less
            # than the previous stamp. But checking for it is OK.
            last_out_time = datetime.strptime(target_cell.value, '%H:%M');

            if(last_out_time < punch_time):
                sheet.update_cell(target_cell.row, target_cell.col, timestamp_str);

    else:
        print("Invalid action: {}", action);

if __name__ == '__main__':

    if(len(sys.argv) >= 2):
        punch_in_out(sys.argv[1]);
    else:
        print('Must supply either SCREEN_UNLOCKED or SCREEN_LOCKED as argument');