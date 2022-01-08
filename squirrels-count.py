import pandas as pd
import pymysql as pms
from connect_db import connect_to_db
import datetime

FILE_PATH = "2018_Central_Park_Squirrel_Census_-_Squirrel_Data.csv"

    
def create_table(conn):
    table_name = "colors"
    sql = '''create table if not exists %s(
        id int not null auto_increment,
        Cinnamon varchar(20) not null,
        White varchar(20) not null,
        Gray varchar(20) not null,
        Cinnamon_white varchar(20) not null,
        Gray_white varchar(20) not null,
        Black_cinnamon_white varchar(20) not null,
        Black varchar(20) not null, 
        Black_white varchar(20) not null,
        Black_cinnamon varchar(20) not null,
        Gray_black varchar(20) not null,
        Time varchar(20) not null,
        Date varchar(20) not null,
        primary key (id)
        ) ''' %table_name
    curs = conn.cursor()
    curs.execute(sql)
    # print("table successfully created")
    curs.close()

def check_connection(conn):
    if conn:
        return True
    else:
        return False

# to get date and time
def get_date_and_time():
    now, date = datetime.datetime.now(), datetime.date.today()
    current_time = now.strftime("%H:%M:%S")
    today = date.strftime("%d/%m/%Y")
    return (current_time, today)
    

# find number of squirrels per fur color
def find_squirrels(column_name, data):
    gray_squirrels = len(data[data[column_name] == 'Gray'])
    cinnamon_squirrels = len(data[data[column_name] == 'Cinnamon'])
    black_squirrels = len(data[data[column_name] == 'Black'])
    return [gray_squirrels, cinnamon_squirrels, black_squirrels]

# convert to a dataframe
def convert_to_dataframe(squirrels_type):
    data_dict = {
        'Fur': ['Gray', 'Cinnamon', 'Black'],
        'Count': [squirrels_type[0], squirrels_type[1], squirrels_type[2]]
    }
    df = pd.DataFrame(data_dict)
    return df

# find highlight Fur color count
def find_squirrels_hightlight_count(column_name, data):
    # find unique color name
    # get rid of Nan value at the first index
    color_dict = {}
    color_list = list(data[column_name].unique())
    del color_list[0]
    for color in color_list:
        color_count = len(data[data[column_name] == color])
        color_dict[color] = color_count
    
    # convert to a data frame
    color_df = pd.DataFrame(color_dict, index=[0])
    return color_df




def main():
    data = pd.read_csv(FILE_PATH)
    first_column = "Primary Fur Color"
    second_column = 'Highlight Fur Color'
    # to drop rows which have Nan value
    # type of squirrels
    data.dropna(subset=[first_column], inplace=True)
    squirrels = find_squirrels(first_column, data)
    df = convert_to_dataframe(squirrels)

    # highlight fur color data frame count
    color_df = find_squirrels_hightlight_count(second_column, data)

    # establish te connection 
    conn = connect_to_db()
    # create table if not exists
    create_table(conn)
    cur = conn.cursor()
    time, date = get_date_and_time()
    sql_query = '''insert into colors(Cinnamon, White, Gray, Cinnamon_white, 
    Gray_white, Black_cinnamon_white, Black, Black_white, Black_cinnamon, Gray_black,
    Time, Date) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

        # testing this
    for row in color_df.itertuples(index=False):     
        colors_num = [str(x) for x in list(row)]
        final_values = tuple(colors_num + [time, date])
        cur.execute(sql_query, final_values)

        cur.close()
   

if __name__=="__main__":
    main()
