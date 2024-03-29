# -*- coding: utf-8 -*-
"""wrangling mini project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mQQUNwMoNqTWwARtN1zRBJdZjAGk0x8V
"""

import pandas as pd
import numpy as np

data_clean = pd.read_csv('clean_data_sample.csv')
data_clean.shape

data_clean.head()

# data ads
data_ads = pd.read_csv('conjoint_survey_ads.csv')
data_ads.shape

data_ads.head()

# data organic
data_organic = pd.read_excel('conjoint_survey_organic.xlsx')
data_organic.shape

data_organic.head()

# join data organic dan ads
df = pd.concat([data_ads, data_organic], axis=0)
df.shape

# reset index
df = df.reset_index(drop=True)
df.head()

# shape
df.head()

# mapping rename kolom
mapping = {'Berapa nomer telepon anda? Nomer ini akan digunakan untuk membagikan GoPay Rp 50.000 per orang, hasil undian untuk 100 orang. Kami hanya akan mengirimkan ke pengisi kuisioner yang valid, i.e. jawaban tidak random.' : 'user_phone',
           '1. Produk manakah yang akan anda beli? (Anda bisa memilih membeli (klik) lebih dari 1 pilihan)' : 'choice1',
           '2. Produk manakah yang akan anda beli? (Anda bisa memilih membeli (klik) lebih dari 1 pilihan)' : 'choice2',
           '3. Produk manakah yang akan anda beli? (Anda bisa memilih membeli (klik) lebih dari 1 pilihan)' : 'choice3',
           '4. Produk manakah yang akan anda beli? (Anda bisa memilih membeli (klik) lebih dari 1 pilihan)' : 'choice4',
           '5. Produk manakah yang akan anda beli? (Anda bisa memilih membeli (klik) lebih dari 1 pilihan)' : 'choice5',
           '6. Produk manakah yang akan anda beli? (Anda bisa memilih membeli (klik) lebih dari 1 pilihan)' : 'choice6',
           '7. Produk manakah yang akan anda beli? (Anda bisa memilih membeli (klik) lebih dari 1 pilihan)' : 'choice7',
           '8. Produk manakah yang akan anda beli? (Anda bisa memilih membeli (klik) lebih dari 1 pilihan)' : 'choice8',
           '9. Produk manakah yang akan anda beli? (Anda bisa memilih membeli (klik) lebih dari 1 pilihan)' : 'choice9',
           '10. Produk manakah yang akan anda beli? (Anda bisa memilih membeli (klik) lebih dari 1 pilihan)' : 'choice10'
}

# rename kolom
df.rename(columns=mapping, inplace=True)

# check data type
df.info()

# change to datatime type
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# check data type
df.info()

# sort by Timestamp
df.sort_values('Timestamp')

# sum duplicate
df.duplicated().sum()

# drop duplicate and keep first
df.drop_duplicates(keep='first')

# drop column timestamp
df = df.drop(columns='Timestamp')

# copy data for comparation
df_copy = df.copy()
df_function = df.copy()

df.head()

"""# Non Function

## Change values choice to list type
"""

# looping each column from dataframe df
for column in df.columns[1:]:

    # looping sum of index 'df'
    for i in range(len(df)):

        # condition if df column each index isin string type
        if isinstance(df.at[i, column], str):

            # split if data is string with comma base on index and column name
            df.at[i, column] = df.at[i, column].split(', ')
        else:

            # if not string then just list values
            df.at[i, column] = []
df.head()

"""## Drop Invalid Data"""

# initial list
selected_rows = []

# looping index and dataframe (itterator rows)
for index, row in df.iterrows():

     # looping column from column index 1 to index end
     for column in df.columns[1:]:

        # variable for obtain rows each columns
        choice_list = row[column]

        # condition if data type is list, and length more than 1 and in the list contains D. Tidak memilih semua product
        if isinstance(choice_list, list) and len(choice_list) > 1 and 'D. Tidak memilih semua product' in choice_list:

            # append index have the condition
            selected_rows.append(index)

# drop the index with have the condition
filtered_df = df.drop(selected_rows)

filtered_df.head()

# check shape after drop invalid rows
print('Dataframe shape', filtered_df.shape)

"""## Change list type values to string type"""

# Back rows contains list to string

# looping index and dataframe (itterator rows)
for index, row in filtered_df.iterrows():

    # looping column from column index 1 to index end
    for column in filtered_df.columns[1:]:

        # variable for obtain rows each columns
        choice_list = row[column]

        # condition if rows is list then split rows in list with comma
        if isinstance(choice_list, list):
            filtered_df.at[index, column] = ', '.join(choice_list)


filtered_df.head()

"""## Transpose rows from horizontal to vertical"""

# Membuat DataFrame baru
new_rows = []

for _, row in filtered_df.iterrows():
    user_phone = row['user_phone']

    for choice_col in filtered_df.columns[1: ]:
        choice_value = row[choice_col]

        # Memeriksa apakah nilai dalam choice_value adalah string
        if isinstance(choice_value, str):
            choices = choice_value.split(', ')

            # looping column choice yang berisi A, B, C
            for choice in ['A', 'B', 'C']:
                if choice in choices:
                    value = 1
                else:
                    value = 0

                # tambahkan hasil tersebut kedalam list
                new_rows.append({'user_phone': user_phone,
                                 'choice': choice,
                                 'new_col': value,
                                 'choice_column': choice_col})

# ubah data dictionary to dataframe
new_df = pd.DataFrame(new_rows)
new_df.head()

# sanichek
df_copy[df_copy['user_phone'] == '08xx8743xxx']

"""## Data validation process transpose"""

# sanichek
new_df[new_df['user_phone'] == '08xx8743xxx']

# Inisialisasi kolom 'calculate' dengan nilai False
function_data = new_df.copy()

function_data['calculate'] = False

# Periksa setiap baris dan setel nilai 'calculate' menjadi True jika kondisinya terpenuhi
for index, row in function_data.iterrows():
    choice_column = row['choice_column']
    choice_value = df_copy.loc[0, choice_column]
    if row['new_col'] == 1 and row['choice'] in choice_value.split(', '):
        function_data.at[index, 'calculate'] = True

filtered_false_condition = function_data[(function_data['calculate'] == True) & (function_data['new_col'] != 1)]
filtered_false_condition

# import pandas as pd

# # Membuat DataFrame df_copy sebagai contoh
# data = {'user_phone': ['08xx8743xxx'],
#         'choice1': ['B'],
#         'choice2': ['A, B']}
# df_copy = pd.DataFrame(data)

# # Membuat DataFrame new_df sebagai contoh
# new_data = {'user_phone': ['08xx8743xxx', '08xx8743xxx', '08xx8743xxx', '08xx8743xxx', '08xx8743xxx', '08xx8743xxx'],
#             'new_col': [0, 1, 0, 1, 1, 0],
#             'choice_column': ['choice1', 'choice1', 'choice1', 'choice2', 'choice2', 'choice2'],
#             'choice': ['A', 'B', 'C', 'A', 'B', 'C']}
# new_data = pd.DataFrame(new_data)

# # Inisialisasi kolom 'calculate' dengan nilai False
# new_data['calculate'] = False

# # Periksa setiap baris dan setel nilai 'calculate' menjadi True jika kondisinya terpenuhi
# for index, row in new_data.iterrows():
#     choice_column = row['choice_column']
#     print(choice_column)
#     choice_value = df_copy.loc[0, choice_column]
#     print(choice_value)
#     if row['new_col'] == 1 and row['choice'] in choice_value.split(', '):
#         new_data.at[index, 'calculate'] = True

"""## Data validation sum of rows"""

# Data validation rows
invalid_user_phone_data = []

for user_phone in new_df['user_phone'].unique():
    user_rows = new_df[new_df['user_phone'] == user_phone]

    if len(user_rows) != 30:

        # Append the user_rows to the invalid_user_phone_data list
        invalid_user_phone_data.append(user_rows)
    else:
        True

invalid_user_phone_data

"""## Matching values with kuisioner item"""

# generate data
generate_mapping = {
    1: {'A': ['Create Analytics Dashboard', 'Tutorial Based', 'Rp. 500.000,0'],
        'B': ['Perform Customer Segmentation', 'Mentoring Based', 'Rp. 350.000,0'],
        'C': ['Design AB Test Experimentation', 'Mentoring Based', 'Rp. 300.000,0'],
        'D': ['', '']},
    2: {'A': ['Create Analytics Dashboard', 'Tutorial Based', 'Rp. 500.000,0'],
        'B': ['Design Data Pipeline', 'Mentoring Based', 'Rp. 300.000,0'],
        'C': ['Perform Credit Scoring Analytics', 'Mentoring Based', 'Rp. 550.000,0'],
        'D': ['', '']},
    3: {'A': ['Perform Customer Segmentation', 'Mentoring Based', 'Rp. 350.000,0'],
        'B': ['Perform Customer Segmentation', 'Tutorial Based', 'Rp. 450.000,0'],
        'C': ['Design Data Pipeline', 'Mentoring Based', 'Rp. 250.000,0'],
        'D': ['', '']},
    4: {'A': ['Design AB Test Experimentation', 'Mentoring Based', 'Rp. 500.000,0'],
        'B': ['Perform Price Optimization', 'Tutorial Based', 'Rp. 350.000,0'],
        'C': ['Perform Credit Scoring Analytics', 'Mentoring Based', 'Rp. 350.000,0'],
        'D': ['', '']},
    5: {'A': ['Design Data Pipeline', 'Mentoring Based', 'Rp. 400.000,0'],
        'B': ['Perform Customer Lifetime Analysis', 'Tutorial Based', 'Rp. 300.000,0'],
        'C': ['Design AB Test Experimentation', 'Tutorial Based', 'Rp. 300.000,0'],
        'D': ['', '']},
    6: {'A': ['Perform Churn Analytics', 'Tutorial Based', 'Rp. 450.000,0'],
        'B': ['Perform Customer Segmentation', 'Mentoring Based', 'Rp. 300.000,0'],
        'C': ['Create Machine Learning Model', 'Mentoring Based', 'Rp. 300.000,0'],
        'D': ['', '']},
    7: {'A': ['Perform Customer Lifetime Analysis', 'Tutorial Based', 'Rp. 500.000,0'],
        'B': ['Design Data Pipeline', 'Mentoring Based', 'Rp. 550.000,0'],
        'C': ['Deploy Machine Learning Model', 'Tutorial Based', 'Rp. 350.000,0'],
        'D': ['', '']},
    8: {'A': ['Perform Credit Scoring Analytics', 'Mentoring Based', 'Rp. 300.000,0'],
        'B': ['Design Data Pipeline', 'Mentoring Based', 'Rp. 550.000,0'],
        'C': ['Create Machine Learning', 'Tutorial Based', 'Rp. 550.000,0'],
        'D': ['', '']},
    9: {'A': ['Create Analytics Dashboard', 'Mentoring Based', 'Rp. 250.000,0'],
        'B': ['Desing AB Test Experimentation', 'Tutorial Based', 'Rp. 550.000,0'],
        'C': ['Perform Customer Lifetime Analysis', 'Mentoring Based', 'Rp. 350.000,0'],
        'D': ['', '']},
    10: {'A': ['Perform Credit Scoring Analytics', 'Mentoring Based', 'Rp. 400.000,0'],
         'B': ['Perform Churn Analytics', 'Mentoring Based', 'Rp. 450.000,0'],
         'C': ['Perform Churn Analytics', 'Tutorial Based', 'Rp. 500.000,0'],
         'D': ['', '']
    }
}

# collect choice_column

# Loop through choice_column from 1 to 10
for i in range(1, 11):

    # looping data by index
    for index, row in new_df.iterrows():

        # condition if column choice is 'A'
        if row['choice_column'] == f'choice{i}' and row['choice'] == 'A':
            option_values = generate_mapping[i]['A']
            new_df.at[index, 'skill'] = option_values[0]
            new_df.at[index, 'bentuk_program'] = option_values[1]
            new_df.at[index, 'harga_program'] = option_values[2]

        # condition if column choice is 'B'
        elif row['choice_column'] == f'choice{i}' and row['choice'] == 'B':
            option_values = generate_mapping[i]['B']
            new_df.at[index, 'skill'] = option_values[0]
            new_df.at[index, 'bentuk_program'] = option_values[1]
            new_df.at[index, 'harga_program'] = option_values[2]

        # condition if column choice is 'C'
        elif row['choice_column'] == f'choice{i}' and row['choice'] == 'C':
            option_values = generate_mapping[i]['C']
            new_df.at[index, 'skill'] = option_values[0]
            new_df.at[index, 'bentuk_program'] = option_values[1]
            new_df.at[index, 'harga_program'] = option_values[2]


new_df.head()

# try 1
a = generate_mapping.get(1, {})['A'][0]
a

# try 2
filtered_data = new_df[(new_df['choice_column'] == 'choice1') & (new_df['choice'] == 'A')]
filtered_data[filtered_data['skill'] == 'Create Analytics Dashboard'].head()

# try 3
filtered_data.choice_column.unique() ,  filtered_data.choice.unique()

# lets try
filtered_data = new_df[(new_df['choice_column'] == 'choice1') & (new_df['choice'] == 'A')]

if (filtered_data['skill'] == 'Create Analytics Dashboard').all() and generate_mapping.get(1, {}).get('A', [0])[0]:
    if (filtered_data['bentuk_program'] == 'Tutorial Based').all() and generate_mapping.get(1, {}).get('A', [0])[1]:
      if (filtered_data['harga_program'] == 'Rp. 500.000,0').all() and generate_mapping.get(1, {}).get('A', [0])[2]:
        print(True)
    else:
        print(False)
else:
    print(False)

# initial result
results = []

# looping data choice column and key dictionary generate_mapping
for key in range(1, 11):

    # looping choice values
    for choice_value in ['A', 'B', 'C']:

        # create filtering data in choice_column and choice
        filtered_data = new_df[(new_df['choice_column'] == f'choice{key}') & (new_df['choice'] == choice_value)]

    # using data filtered_data
    # create condition if 'key' generate_mapping condition equal with filtered_data
    # in column 'skill', 'bentuk program', and harga_promo
    # assumed all() because output is boolean
        if (filtered_data['skill'] == generate_mapping.get(key, {}).get(choice_value, [0])[0]).all() and \
            (filtered_data['bentuk_program'] == generate_mapping.get(key, {}).get(choice_value, [0])[1]).all() and \
            (filtered_data['harga_program'] == generate_mapping.get(key, {}).get(choice_value, [0])[2]).all():

            # variable if condition true
            result = f"Key {key}, Choice {choice_value}: True"

            # append boolean true to results with list type
            results.append(result)

        else:
            # variable if condition false
            result = f"Key {key}, Choice {choice_value}: False"

            # append boolean true to results with list type
            results.append(result)

results

# sanichek
new_df[new_df['user_phone'] == '08xx17856xxx']

"""# Function"""

def rows_to_list(data):
  """
  This function for change rows data to list in each choice
  for check preaper remove rows invalid

  Parameters :
  ------------
  data : pd.DataFrame
    data input for change to list

  return :
  --------
    result of return data to list each rows
  """
  # looping each column from dataframe df
  for column in df.columns[1:]:

      # looping sum of index 'df'
      for i in range(len(data)):

          # condition if df column each index isin string type
          if isinstance(data.at[i, column], str):

              # split if data is string with comma base on index and column name
              data.at[i, column] = data.at[i, column].split(', ')
          else:

              # if not string then just list values
              data.at[i, column] = []
  return data

def delete_invalid_rows(data_rows_list) :
  """
  Function for delete invalid condition example : if choice contains (D, B)
  then invalid data

  Paramaters :
  ------------
  data_rows_list : pd.DataFrame
    Input data contains list data from function rows_to_list

  return :
  --------
    result after find the invalid data and the drop the rows invalid
  """
  # initial list
  selected_rows = []

  # looping index and dataframe (itterator rows)
  for index, row in data_rows_list.iterrows():

      # looping column from column index 1 to index end
      for column in data_rows_list.columns[1:]:

          # variable for obtain rows each columns
          choice_list = row[column]

          # condition if data type is list, and length more than 1 and
          # in the list contains D. Tidak memilih semua product
          if isinstance(choice_list, list) and len(choice_list) > 1 \
              and 'D. Tidak memilih semua product' in choice_list:

              # append index have the condition
              selected_rows.append(index)

  # drop the index with have the condition
  filtered_df = data_rows_list.drop(selected_rows)

  return filtered_df

def rows_to_string(data_list):
  """
  Function for change rows from list to string

  Parameters :
  ------------
  data_after_invalid : pdf.DataFrame
    Input data contains list data from function data_rows_list

  return :
  --------
    result data after change from list type to string
  """
  # looping index and dataframe (itterator rows)
  for index, row in data_list.iterrows():

      # looping column from column index 1 to index end
      for column in data_list.columns[1:]:

          # variable for obtain rows each columns
          choice_list = row[column]

          # condition if rows is list then split rows in list with comma
          if isinstance(choice_list, list):
              data_list.at[index, column] = ', '.join(choice_list)

  return data_list

def transpose_data(data_transpose, index_column):
  """
  Function for split each values if have more than choice, and then transpose
  each columns choice to one columns

  Parameters :
  ------------
  data_transpose : pd.Dataframe
    data input from function rows_to_string

  return :
  --------
    result after transpose data with dictionary type then change to dataframe
  """
  # Membuat DataFrame baru
  new_rows = []

  for _, row in filtered_df.iterrows():
      user_phone = row[index_column]

      for choice_col in filtered_df.columns[1: ]:
          choice_value = row[choice_col]

          # Memeriksa apakah nilai dalam choice_value adalah string
          if isinstance(choice_value, str):
              choices = choice_value.split(', ')

              # looping column choice yang berisi A, B, C
              for choice in ['A', 'B', 'C']:
                  if choice in choices:
                      value = 1
                  else:
                      value = 0

                  # tambahkan hasil tersebut kedalam list
                  new_rows.append({'user_phone': user_phone,
                                  'choice': choice,
                                  'new_col': value,
                                  'choice_column': choice_col})

  # ubah data dictionary to dataframe
  new_df = pd.DataFrame(new_rows)

  return new_df

def validation_rows(data_validation_rows, unique_column):
  """
  Function for check each length of rows each user_phone

  Parameters :
  ------------
  data_validation_rows : pd.DataFrame
    input data from function data_transpose

  return :
  --------
    result if the rows not 30 then show data which has been not equal 30, else
  justshow empty list
  """
  # Data validation rows
  invalid_user_phone_data = []

  for user_phone in new_df[unique_column].unique():
      user_rows = new_df[new_df[unique_column] == user_phone]

      # condition if length of user_rows not 30
      if len(user_rows) != 30:

          # Append the user_rows to the invalid_user_phone_data list
          invalid_user_phone_data.append(user_rows)
      else:
          True

  return invalid_user_phone_data

def matching_values(current_data, previous_data):
  """
  Function for check matching data after transpose data with previous data which
  has not been transpose

  Parameters :
  ------------
  current_data : pd.DataFrame
    input data from function data_transpose

  previous_data : pd.DataFrame
    input data without transpose data

  return :
  --------
    return data that has condition True but not contains 1
  """
  # Inisialisasi kolom 'calculate' dengan nilai False
  function_data = current_data.copy()

  # Selanjutnya, kolom calculate akan di isi false jika tidak memenuhi kondisi
  function_data['calculate'] = False

  # looping index and dataframe (itterator rows)
  for index, row in function_data.iterrows():

      # Ambil nilai dari kolom 'choice_column' pada baris saat ini
      choice_column = row['choice_column']

      # Ambil nilai dari 'choice_column' pada baris saat ini dari DataFrame 'previous_data'
      choice_value = previous_data.loc[0, choice_column]

      # Periksa apakah nilai 'new_col' pada baris saat ini adalah 1
      # dan apakah nilai 'choice' ada dalam daftar nilai yang dipisahkan oleh
      # koma dari 'choice_value'
      if row['new_col'] == 1 and row['choice'] in choice_value.split(', '):

          # Jika kondisi terpenuhi, atur nilai 'calculate' pada rows current_data menjadi True
          function_data.at[index, 'calculate'] = True

  # Filter baris yang memiliki 'calculate' True dan 'new_col' tidak sama dengan 1
  filtered_false_condition = function_data[(function_data['calculate'] == True)\
                                        & (function_data['new_col'] != 1)]

  return filtered_false_condition

def generate_data(data_generate, generate_mapping):
  """
  If the validation function before have not a problem Function for change
  the values each choice A, B, C to genarate mapping which has been
  created previously

  Parameters :
  ------------
  data_generate : pd.Dataframe
    input data from function transpose_data

  generate_mapping : dictionary
    mapping data for change the values in each rows data_generate

  return :
  --------
    the result have 3 new columns which contains generate_mapping
  """
  # Loop through choice_column from 1 to 10
  for i in range(1, 11):

      # looping data by index
      for index, row in data_generate.iterrows():

          # condition if column choice is 'A'
          if row['choice_column'] == f'choice{i}' and row['choice'] == 'A':
              option_values = generate_mapping[i]['A']
              data_generate.at[index, 'skill'] = option_values[0]
              data_generate.at[index, 'bentuk_program'] = option_values[1]
              data_generate.at[index, 'harga_program'] = option_values[2]

          # condition if column choice is 'B'
          elif row['choice_column'] == f'choice{i}' and row['choice'] == 'B':
              option_values = generate_mapping[i]['B']
              data_generate.at[index, 'skill'] = option_values[0]
              data_generate.at[index, 'bentuk_program'] = option_values[1]
              data_generate.at[index, 'harga_program'] = option_values[2]

          # condition if column choice is 'C'
          elif row['choice_column'] == f'choice{i}' and row['choice'] == 'C':
              option_values = generate_mapping[i]['C']
              data_generate.at[index, 'skill'] = option_values[0]
              data_generate.at[index, 'bentuk_program'] = option_values[1]
              data_generate.at[index, 'harga_program'] = option_values[2]

  return data_generate

def final_validation(data_generate, generate_mapping):
    """
    Function for validation after matching data with reference values is equals

    Parameters :
    ------------
    data_generate : pd.DataFrame
      input data after matching data with reference dictionary data

    generate_mapping : dictionary and list type
      input dictionary data for validation after matching data

    return :
    --------
      resul validation if true or false will added in initial result with
    list type
    """
    # initial result
    results = []

    # looping data choice column and key dictionary generate_mapping
    for key in range(1, 11):

        # looping choice values
        for choice_value in ['A', 'B', 'C']:

            # create filtering data in choice_column and choice
            filtered_data = data_generate[(data_generate['choice_column'] == f'choice{key}') \
                                          & (data_generate['choice'] == choice_value)]

        # using data filtered_data
        # create condition if 'key' generate_mapping condition equal with filtered_data
        # in column 'skill', 'bentuk program', and harga_promo
        # assumed all() because output is boolean
            if (filtered_data['skill'] == generate_mapping.get(key, {}).get(choice_value, [0])[0]).all() and \
               (filtered_data['bentuk_program'] == generate_mapping.get(key, {}).get(choice_value, [0])[1]).all() and \
               (filtered_data['harga_program'] == generate_mapping.get(key, {}).get(choice_value, [0])[2]).all():

                # variable if condition true
                result = f"Key {key}, Choice {choice_value}: True"

                # append boolean true to results with list type
                results.append(result)

            else:
                # variable if condition false
                result = f"Key {key}, Choice {choice_value}: False"

                # append boolean true to results with list type
                results.append(result)

    return results

data_list_result = rows_to_list(data=df_function)
delete_invalid_result = delete_invalid_rows(data_rows_list=data_list_result)
rows_to_string = rows_to_string(data_list=delete_invalid_result)
data_transpose = transpose_data(data_transpose = rows_to_string,
                                index_column = 'user_phone' )

data_transpose.head()

# validation each user must have 30 rows
data_validation_rows = validation_rows(data_validation_rows = data_transpose,
                                       unique_column = 'user_phone')
# validation matching data
matching_values = matching_values(current_data = data_transpose,
                                  previous_data = df_copy)
print('Data Validation Sum of Rows')
data_validation_rows
print('')
print('Data Validation not True matching condition')
matching_values

# generate data
generate_mapping = {
    1: {'A': ['Create Analytics Dashboard', 'Tutorial Based', 'Rp. 500.000,0'],
        'B': ['Perform Customer Segmentation', 'Mentoring Based', 'Rp. 350.000,0'],
        'C': ['Design AB Test Experimentation', 'Mentoring Based', 'Rp. 300.000,0'],
        'D': ['', '']},
    2: {'A': ['Create Analytics Dashboard', 'Tutorial Based', 'Rp. 500.000,0'],
        'B': ['Design Data Pipeline', 'Mentoring Based', 'Rp. 300.000,0'],
        'C': ['Perform Credit Scoring Analytics', 'Mentoring Based', 'Rp. 550.000,0'],
        'D': ['', '']},
    3: {'A': ['Perform Customer Segmentation', 'Mentoring Based', 'Rp. 350.000,0'],
        'B': ['Perform Customer Segmentation', 'Tutorial Based', 'Rp. 450.000,0'],
        'C': ['Design Data Pipeline', 'Mentoring Based', 'Rp. 250.000,0'],
        'D': ['', '']},
    4: {'A': ['Design AB Test Experimentation', 'Mentoring Based', 'Rp. 500.000,0'],
        'B': ['Perform Price Optimization', 'Tutorial Based', 'Rp. 350.000,0'],
        'C': ['Perform Credit Scoring Analytics', 'Mentoring Based', 'Rp. 350.000,0'],
        'D': ['', '']},
    5: {'A': ['Design Data Pipeline', 'Mentoring Based', 'Rp. 400.000,0'],
        'B': ['Perform Customer Lifetime Analysis', 'Tutorial Based', 'Rp. 300.000,0'],
        'C': ['Design AB Test Experimentation', 'Tutorial Based', 'Rp. 300.000,0'],
        'D': ['', '']},
    6: {'A': ['Perform Churn Analytics', 'Tutorial Based', 'Rp. 450.000,0'],
        'B': ['Perform Customer Segmentation', 'Mentoring Based', 'Rp. 300.000,0'],
        'C': ['Create Machine Learning Model', 'Mentoring Based', 'Rp. 300.000,0'],
        'D': ['', '']},
    7: {'A': ['Perform Customer Lifetime Analysis', 'Tutorial Based', 'Rp. 500.000,0'],
        'B': ['Design Data Pipeline', 'Mentoring Based', 'Rp. 550.000,0'],
        'C': ['Deploy Machine Learning Model', 'Tutorial Based', 'Rp. 350.000,0'],
        'D': ['', '']},
    8: {'A': ['Perform Credit Scoring Analytics', 'Mentoring Based', 'Rp. 300.000,0'],
        'B': ['Design Data Pipeline', 'Mentoring Based', 'Rp. 550.000,0'],
        'C': ['Create Machine Learning', 'Tutorial Based', 'Rp. 550.000,0'],
        'D': ['', '']},
    9: {'A': ['Create Analytics Dashboard', 'Mentoring Based', 'Rp. 250.000,0'],
        'B': ['Desing AB Test Experimentation', 'Tutorial Based', 'Rp. 550.000,0'],
        'C': ['Perform Customer Lifetime Analysis', 'Mentoring Based', 'Rp. 350.000,0'],
        'D': ['', '']},
    10: {'A': ['Perform Credit Scoring Analytics', 'Mentoring Based', 'Rp. 400.000,0'],
         'B': ['Perform Churn Analytics', 'Mentoring Based', 'Rp. 450.000,0'],
         'C': ['Perform Churn Analytics', 'Tutorial Based', 'Rp. 500.000,0'],
         'D': ['', '']
    }
}

# final data cleaning
matching_data =generate_data(data_generate = data_transpose,
                             generate_mapping = generate_mapping)
matching_data

# final validation
final_validation(data_generate = matching_data,
                 generate_mapping = generate_mapping)

# drop columns not used
matching_data = matching_data.drop(columns=['choice_column', 'choice'])

# rename data
matching_data = matching_data.rename(columns = {'new_col':'choice'})

# save data
matching_data.to_csv('data_clean_conjoint.csv', index=False)

# data clean
matching_data