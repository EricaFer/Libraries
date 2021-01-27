def rs(df, col, perc = True, dividendo = 0, n_stock = 1, tax_buy = 0, tax_sell = 0, gains = False):

    '''
    Input: 
    - df : dataframe
    - col: column to be processed
    - perc: if True, returns the tax percentage

    Process:
        Given that the Simple Return Tax is calculated by:

        Lucro = (preço final - preço inicial + dividendo) * num de ações - ( taxa de compra + taxa de venda)

        RS ( Retorno Simples) = Lucro*100 / ( preço inicial + taxa de compra)

        this is calculated.

    Output:

    - Taxa de Retorno Simples
    - if lucro is True, returns Lucro as well

    '''

    def gains():
        # Calculates the gains
        returns (df[col][-1:] - df[col][0] + dividendo) * n_stock - (tax_sell + tax_sell)

    tax = gains() / (df[col][-1:] + df[col][0])

    if perc is True:
        tax = tax * 100

    if gains is True:
        return (tax, gains)
    
    else:
        return tax

def rs_daily(df,col):
    df['RS' + col] = (df[col] / df[col].shift(1) - 1)

def wallet_importer(df_name, stock_names, source = 'yahoo', start = '2015-01-01', col = 'Adj Close'):
    
    for acao in stock_names:
        df_name[acao] = data.DataReader(acao,
                                   data_source = source,
                                   start = start)[col]

def rl(df, dividendo = 0, n_stock = 1, tax_buy = 0, tax_sell = 0):
    for col in df.columns:
        if col != 'Date':
            if col[:2] != 'RS':
                df['RL ' +  col] = np.log(df[col] * n_stock + dividendo - tax_sell / df[col].shift(1) * n_stock + tax_buy) * 100

def rs_anual(df):
    anual_dict = {}
    for col in df.columns:
        if col[:2] == 'RS':
            anual_dict['Taxa Anual ' + col[3:]] = (df[col].mean() * 246) * 100
    
    return anual_dict                

def rl_total(df):
    rl = {}
    for col in df.columns:
        if col != 'Date':
            if col[:2] != 'RS':
                rl['RL ' +  col] = np.log(df[col][len(df) - 1] / df[col][0]) * 100
    return rl

def wallet_importer(source = 'yahoo', start = '2015-01-01',df, stock_names, file):
    
    for acao in stock_names:
        df[acao] = data.DataReader(acao,
                                   data_source = source,
                                   start = start)[col]
    df.to_csv(files)

def rename(df, name):
    
    i = 0

    for col in df.columns:
        if col != 'Date':
            df.rename(columns = {col : name[i]}, inplace = True)
            i += 1

def null_deleter(*args):
    null_rows = []
    
    #Checando cada linha de cada DataFrame
    for df in args:
        for index, row in df.iterrows():
            is_nan = row.isnull()
            if is_nan.any():
                if index not in null_rows:
                    null_rows.append(index)
                    
        df.drop(null_rows, inplace = True)

def price_normalizer(*args):
    '''
    Input: múltiplos DataFrames
    
    Process: Itera as colunas e divide o valor atual pelo valor inicial
    
    Output: DataFrames atualizados
    '''
    for df in args:
        for i in df.columns[1:]:
            df[i] = df[i]/df[i][0]

def wallet_plot(*args, 
                 subplot_titles = ['Carteira 1', 'Carteira 2'], 
                 Title = 'Histórico do preço das ações'):
    
    '''
    Input: 
    - args: múltiplos DataFrames
    - subplot_titles: títulos do subplot
    - Title: título do gráfico
    
    Process:
    - cria especificação do gráfico
    - itera por DataFrame e cria um subplot
    - itera as colunas do DataFrame e adiciona a linha
    
    Output:
    - Gráfico
    '''
    
    fig = make_subplots(rows = len(args),
                        cols = 1,
                        shared_xaxes = True,
                        start_cell = 'top-left',
                        subplot_titles = subplot_titles,
                        horizontal_spacing= 0,
                        vertical_spacing= 0.1,
                        x_title = 'Data',
                        y_title = 'Valorização')
    
    j = 1
    for df in args:
        for i in df.columns[1:]:
            
            fig.add_trace(go.Scatter(x = df.Date,
                                        y = df[i],
                                        name = i),
                                        row = j,
                                        col = 1)
        j += 1

    fig.update_layout(title = Title, title_x = 0.5)
    fig.show()

def norm_wallet(*args, x_col = 'Date', y_col = 'Normalização', nome = ['Carteira 1', 'Carteira 2']):
    
    i = 0
    fig = px.line()
    
    for df in args:
        df['Total'] = df.sum(axis = 1) 
        df[y_col] = df.Total / df.Total[0]

def wallet_comparer(df, col = 'Normalização'):

    fig = px.line()

    for i in range(0,2):
        
        fig.add_scatter(x = df[i].Date, 
                        y = df[i][col], 
                        name = i + 1)
        
    fig.update_layout(title = 'Comparando Carteiras', 
                    title_x=0.5,
                    xaxis_title = 'Data',
                    yaxis_title = 'Variação do Capital',
                    legend_title = 'Carteira',
                    font = dict( size = 15))

def norm_plot(df):

    figura = px.line()

    for i in df.columns[1:]:
        figura.add_scatter(x = df.Date, y = df[i], name = i)
        
    figura.update_layout(title = 'Histórico do preço das ações normalizado', title_x=0.5)