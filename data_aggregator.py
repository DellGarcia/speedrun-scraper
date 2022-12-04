import pandas as pd
from os import walk, path, makedirs


def agregate_game_data():
    pd.set_option('display.max_columns', None)

    game_name = 'Hollow_Knight'

    # folder path
    dir_path = rf'games\{game_name}'

    # list to store files name
    for (dir_path, dir_names, file_names) in walk(dir_path):
        dirs = dir_path.split('\\')

        if len(file_names) > 0:
            # print(dir_path, dir_names, file_names)
            df_list = []
            for name in file_names:
                df = pd.read_csv(path.join(dir_path, name), sep=',')

                for i in range(2, len(dirs), 1):
                    aux_df = pd.DataFrame()
                    aux_df[f'Categoria {i-1}'] = pd.Series([dirs[i] for _ in range(len(df))])
                    df = df.join(aux_df)

                df_list.append(df)

            if len(file_names) == 4:
                final_df = pd.concat(df_list)
                print(final_df.head(20))
                # print(final_df.info())

            name = ''
            for d in range(2, len(dirs), 1):
                name += dirs[d] + '-'

            result_path = f'results/{game_name}'

            if not path.exists(result_path):
                makedirs(result_path)

            final_df = pd.concat(df_list)
            final_df.to_csv(f'{result_path}/{name}.csv')
            # print(final_df.head())
