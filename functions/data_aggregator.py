import pandas as pd
import glob
import re
import matplotlib.pyplot as plt
import seaborn as sns

from shutil import rmtree
from os import walk, path, makedirs
from datetime import datetime
    

pd.set_option('display.max_columns', None)


def aggregate_game_data(game_name):
    dir_path = f"games/{game_name}".lower()
    result_path = f'results/{game_name}'.lower()

    if not path.exists(dir_path):
        print(f'A pasta {dir_path} não foi encontrada...')
        print('O arquivo data_scrapper deve ser executado primeiro!')

    if path.exists(result_path):
        rmtree(result_path, ignore_errors=False, onerror=None)

    for (dir_path, dir_names, file_names) in walk(dir_path):
        dirs = dir_path.split('\\')
    
        if len(file_names) > 0:
            df_list = []
            for name in file_names:
                df = pd.read_csv(path.join(dir_path, name), sep=',')

                for i in range(1, len(dirs), 1):
                    aux_df = pd.DataFrame()
                    aux_df[f'{dirs[i]}'] = pd.Series([dirs[i] for _ in range(len(df))])
                    df = df.join(aux_df)

                df_list.append(df)

            name = ''
            for d in range(1, len(dirs), 1):
                name += dirs[d] + '-'

            if not path.exists(result_path):
                makedirs(result_path)

            final_df = pd.concat(df_list)
            final_df.to_csv(f'{result_path}/{name}.csv', mode='w', encoding='utf-8')


def covert_to_date(date_string):
    try:
        hour_parts = re.sub('[^0-9 ]', '', date_string).split(' ')[::-1]
        part_types = re.sub('[^a-z ]', '', date_string).upper().split(' ')[::-1]

        if 'MS' in part_types:
            part_types[0] = 'f'
        
        for i in range(len(part_types)):
            if part_types[i].lower() == 'h':
                hour = int(hour_parts[i])
                if hour >= 24:
                    part_types.append('d')
                    hour_parts.append(int(hour / 24))
                    hour_parts[i] = int(hour % 24)

        hour_string = ' '.join([f'{str(x).zfill(2)}' for x in hour_parts])
        part_format = ' '.join([f'%{s}' for s in part_types])

        initial = datetime(1900, 1, 1, 0, 0, 0, 0)

        delta = (datetime.strptime(hour_string, part_format) - initial).total_seconds() / 60

        return round(delta)
        # return datetime.strptime(hour_string, part_format)
        # return datetime.strptime(hour_string, '%M %S')
    except TypeError as err:
        print(f"Erro: {err}")
        print(f'Deu ruin: {date_string}')
    

def plot_series(serie, game_name):
    country = []
    mean_time = []

    for k in serie.keys():
        country.append(k)
        mean_time.append(serie[k])
    
    df = pd.DataFrame(list(zip(country, mean_time)), columns=['Country', 'Value'])
    res = df.head(6).sort_values(by='Value')

    mean_time_barplot = sns.barplot(data=res, x='Country', y='Value')
    mean_time_barplot.set(title='País x Média de tempo')
    mean_time_barplot.set(xlabel='País', ylabel='Média de tempo')
    
    plt.savefig(f'results/{game_name}/summary/pais-x-media-de-tempo.png')
    plt.figure().clear()

def summarize_game_data(game_name):
    result_path = f'results/{game_name}'.lower()

    all_files = glob.glob(result_path + "/*.csv")

    df_list = []

    for filename in all_files:
        df_list.append(pd.read_csv(filename, index_col=None, header=0))

    df = pd.concat(df_list, axis=0, ignore_index=True)

    if not path.exists(f'{result_path}/summary/'):
        makedirs(f'{result_path}/summary/')

    df.to_csv(f'{result_path}/summary/result.csv', mode='w', encoding='utf-8')
    create_plot_visualization(df, game_name)
    

def create_plot_visualization(df, game_name):
    ''' Países que mais submetem runs '''
    filtered_df = df[df['Country'] != 'unknown']
    country_runs = filtered_df['Country'].value_counts(ascending=False).reset_index(name='values').head(5)
    
    country_barplot = sns.barplot(data=country_runs, x='index', y='values')
    country_barplot.set(title='País x Submissões')
    country_barplot.set(xlabel='País', ylabel='Submissões')

    plt.savefig(f'results/{game_name}/summary/pais-x-submissoes.png')
    plt.figure().clear()
 
    ''' Console mais utilizado '''
    filtered_df = df[['console_runs', 'Platform']]
    filtered_df = filtered_df.dropna(subset=['console_runs'])
 
    platform_runs = filtered_df['Platform'].value_counts(ascending=False).reset_index(name='values')

    console_barplot = sns.barplot(data=platform_runs, x='index', y='values')
    console_barplot.set(title='Console x Submissões')
    console_barplot.set(xlabel='Console', ylabel='Submissões')

    plt.savefig(f'results/{game_name}/summary/console-x-submissoes.png')
    plt.figure().clear()

    ''' Média de tempo por país (Considerando as 500 melhores submissoes) '''
    df2 = df[['LRT', 'Country']]
    df2 = df2.dropna(subset=['LRT'])
    
    df2 = df2[df2['Country'] != 'unknown']
    # Transformando a coluna em minutos (int)
    df2['LRT'] = df2['LRT'].apply(lambda x: covert_to_date(x))

    df2 = df2.sort_values(by=['LRT']).head(500)

    # Remove outliers for LRT
    desc = df2['LRT'].describe()
    q3 = desc[6]
    df2 = df2[df2['LRT'] <= q3]

    df2.groupby(by=['Country'], group_keys=False).mean().apply(lambda x: plot_series(x, game_name))
