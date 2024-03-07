import json
import sys
from datetime import datetime, timedelta, timezone

from xlsxwriter import Workbook

def make_xlsx(input_file_name, output_file_name, list_key_name):
    with open(input_file_name, 'r') as f:
        resp = f.read()

    resp = json.loads(resp)    

    if not list_key_name:
        dict_list = resp
    else:
        dict_list = resp[list_key_name]

    ordered_list= list(dict_list[0].keys())

    wb=Workbook(output_file_name)
    ws=wb.add_worksheet("sheet1")

    first_row=0
    for header in ordered_list:
        col=ordered_list.index(header) 
        ws.write(first_row,col,header)

    row=1
    for entry in dict_list:
        for _key,_value in entry.items():
            col=ordered_list.index(_key)
            if type(_value) == list:
                _value = str(_value)
            
            # if _key == "time":
            #     utc_time = datetime.fromtimestamp(int(_value / 1000), timezone.utc)                
            #     kst_time = utc_time + timedelta(hours=9)                
            #     formatted_time = kst_time.strftime('%Y-%m-%d %H-%M-%S')
            #     _value = formatted_time
                
            ws.write(row,col,_value)
        row+=1
    wb.close()


if __name__ == '__main__':
    list_key_name = sys.argv[3] if len(sys.argv) > 3 else None

    make_xlsx(
        input_file_name=sys.argv[1],
        output_file_name=sys.argv[2],
        list_key_name=list_key_name
    )

# How to use
# - python main.py data.json output.xlsx
#
# Example input data
# [
#     {
#         "a": 10,
#         "b": 20
#     },
#     ...
# ] 