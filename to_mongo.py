import pandas as pd
import json
from itertools import groupby
import pymongo
import re
import sys



def get_index_dict(filename):

    df = pd.read_csv(filename)
    # turn the type of content into list
    df.content = df.content.apply(lambda x: [w.strip("''[]") for w in x.split(', ')])

    term_dic = {}

    for i in df.index:

        content_list = df.iloc[i,-1]

        for j in range(len(content_list)):
            word = content_list[j]
            doc_id = str(df.iloc[i,0])

            if word not in term_dic.keys():
                pos_list = [str(j+1)]
                doc_dict = {doc_id: pos_list}
                term_dic[word] = doc_dict

            else:
                if doc_id not in term_dic[word].keys():
                    term_dic[word][doc_id] = [str(j+1)]

                else:
                    term_dic[word][doc_id].append(str(j+1))

    sorted_term_dic = dict(sorted(term_dic.items(),key=lambda item:item[0]))

    return sorted_term_dic



def write_to_file(term_dic,file_name):

    with open(file_name, 'w', encoding='gb18030') as f:
        for key, value in term_dic.items():
            f.write(str(key)+':\n')
            for innerkey, innervalue in value.items():
                f.write('\t'+ str(innerkey)+': ')
                f.write(','.join('%s' %pos for pos in innervalue) + '\n')
            f.write('\n')
    f.close()


myclient = pymongo.MongoClient("8.209.74.127:27017")

mydb = myclient["reverseIndex"]
mycol = mydb["index"]

# input_list = ['df0.csv', 'df1.csv']

input_list = sys.argv[1:]

print(str(input_list))

for file in input_list:

    print(file + "...")

    term_dic = get_index_dict(file)
    output_txt = 'index' + re.findall(r'\d+', file)[0] + 'txt'
    write_to_file(term_dic, output_txt)

    for key, value in term_dic.items():
        if mycol.find_one({'word': key}) == None:
            mydict = {'word': key, 'position': value}
            x = mycol.insert_one(mydict)

        else:
            old_value = mycol.find_one({'word': key})['position']
            old_value.update(value)
            x = mycol.update_one({'word': key},
                                 {'$set': {'position': old_value}})






