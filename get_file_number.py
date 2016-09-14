import pandas as pd
import StringIO

df = pd.read_csv(StringIO.StringIO(file_list),
                   header=None,
                   comment='T',
                   sep=r'\s*',
                   names=['file_number', 'img_number', 'rd_col', 'file_size', 'kb_col', 'file_type'],
                   usecols=['file_number', 'img_number', 'file_type'],
                   escapechar='\#')

df = df.dropna(how='any')
df = df[df.file_type == 'image/jpeg']
df.file_number = df.file_number.str[1:]
df.file_number = df.file_number.convert_objects(convert_numeric=True)
df.img_number = df.img_number.str.replace('[^0-9]', '').astype(float)

high_filenumber = df.file_number[df.img_number.idxmax()]
