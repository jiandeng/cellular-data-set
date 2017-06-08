from base64 import b64decode as de
from struct import unpack
import pandas as pd
import numpy as np
import operator
import sys

def cell_to_dataframe(file):
    f = open(file)
    content = f.readlines()
    f.close()

    content = map(lambda x: x if '-->>' not in x else x[25:], content)
    records = [ unpack('i'*33, de(line[:-1], '-/'))[1:-3] for line in content ]
    cn = ['sn', 'start_time', 'hwt_time', 'csq_time', 'creg_time', 'csq', 'pdp_time', 'connect_time']
    cn.extend(['upload_time' + str(i) for i in range(10)])
    cn.extend(['download_time' + str(i) for i in range(10)])
    cn.append('voltage')
    df = pd.DataFrame(records, columns=cn)

    cn = ['sn', 'start_time', 'hwt_time', 'csq_time', 'creg_time', 'csq', 'pdp_time', 'connect_time']
    cn.extend(reduce(operator.concat, [['upload_time' + str(i), 'download_time' + str(i)] for i in range(10)]))
    cn.append('voltage')
    df = df[cn]

    df.where(df != -1, np.nan, inplace=True)
    for col in df:
        if col != 'start_time' and 'time' in col:
            df[col] -= df['start_time']

    return df


if __name__ == '__main__':
    df = cell_to_dataframe(sys.argv[1])
    print df.tail()


