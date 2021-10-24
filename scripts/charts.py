import time
import numpy as np
import numpy.linalg as linalg
import scipy.sparse as sparse
import matplotlib.pyplot as plt
from scipy.sparse.linalg import lsqr
from scipy.sparse import coo_matrix
from datetime import datetime

acronym_dict = {
    "ACRE": "AC",
    "ALAGOAS": "AL",
    "AMAPÁ": "AP",
    "AMAZONAS": "AM",
    "BAHIA": "BA",
    "CEARÁ": "CE",
    "DISTRITO FEDERAL": "DF",
    "ESPÍRITO SANTO": "ES",
    "GOIÁS": "GO",
    "MARANHÃO": "MA",
    "MATO GROSSO": "MT",
    "MATO GROSSO DO SUL": "MS",
    "MINAS GERAIS": "MG",
    "PARANÁ": "PR",
    "PARAÍBA": "PB",
    "PARÁ": "PA",
    "PERNAMBUCO": "PE",
    "PIAUÍ": "PI",
    "RIO DE JANEIRO": "RJ",
    "RIO GRANDE DO NORTE": "RN",
    "RIO GRANDE DO SUL": "RS",
    "RONDÔNIA": "RO",
    "RORAIMA": "RR",
    "SANTA CATARINA": "SC",
    "SERGIPE": "SE",
    "SÃO PAULO": "SP",
    "TOCANTINS": "TO"
}

def extract_per_state_per_month_csv(csv_file: str, delimiter=","):
    uf_dict = {}

    with open(csv_file, "r", encoding="utf-8") as f:
        count_lines = 0

        while True:
            line = f.readline()

            count_lines += 1

            if count_lines == 1:
                continue

            elif not line:
                break
            
            arr = line.split(delimiter)
            
            uf = arr[0].strip()
            date = arr[2]
            qnt = int(arr[3])
            
            if uf not in uf_dict:
                uf_dict[uf] = {}
            
            if date not in uf_dict[uf]:
                uf_dict[uf][date] = 0
            
            uf_dict[uf][date] += qnt
    
    return uf_dict 

def extract_total_price_per_state_csv(csv_file: str, delimiter=","):
    total_price_list = []

    with open(csv_file, "r", encoding="utf-8") as f:
        count_lines = 0

        while True:
            line = f.readline()

            count_lines += 1

            if count_lines == 1:
                continue

            elif not line:
                break
            
            arr = line.split(delimiter)
            
            uf = arr[0].strip()
            price = float(arr[1])

            total_price_list.append((uf, price))

    total_price_list.sort(key=lambda x : x[1], reverse=False)

    return total_price_list 

def extract_vent_types_per_state_csv(csv_file: str, delimiter=","):
    uf_dict = {}

    with open(csv_file, "r", encoding="utf-8") as f:
        count_lines = 0

        while True:
            line = f.readline()

            count_lines += 1

            if count_lines == 1:
                continue

            elif not line:
                break
            
            arr = line.split(delimiter)
            
            uf = arr[0].strip()
            type = arr[1].strip()
            qnt = int(arr[2].strip())

            if uf not in uf_dict:
                uf_dict[uf] = [0, 0]
            
            if "ICU" in type:
                uf_dict[uf][0] = qnt
            else:
                uf_dict[uf][1] = qnt


    return uf_dict 

def extract_total_price_per_state_per_pop_csv(csv_file: str, delimiter=","):
    total_price_list = []

    with open(csv_file, "r", encoding="utf-8") as f:
        count_lines = 0

        while True:
            line = f.readline()

            count_lines += 1

            if count_lines == 1:
                continue

            elif not line:
                break
            
            arr = line.split(delimiter)
            
            uf = arr[0].strip()
            price = float(arr[3]) * 100

            total_price_list.append((uf, price))

    total_price_list.sort(key=lambda x : x[1], reverse=False)

    return total_price_list 

def bar_x_state_y_date(dt_dict: dict, item: str, date: str, color: str="blue", dx = -0.4, dy=500):
    x = []
    y = []

    count = 1
    for uf, dates in dt_dict.items():
        x.append(count)
        count += 1
        if date in dates:
            y.append(dates[date])
        else:
            y.append(0)
    
    fig, ax = plt.subplots(1, 1, figsize=(20, 10), dpi=80)

    for index, value in enumerate(x):    
        if y[index] == 0:
            continue
        else: 
            ax.text(value +dx, y[index] + dy, y[index])


    ax.set_ylabel("Quantidade de {0}".format(item, date))
    ax.bar(x, y, color=color, tick_label=list(map(lambda x : acronym_dict[x], dt_dict.keys())))
    
    plt.title("Quantidade de {0} comprada no mês {1}".format(item, date))
    plt.xticks(x)

    plt.show()

def bar_x_date_y_state(dt_dict: dict, item: str, state: str, color: str="blue", dx = -0.4, dy=500):
    x = []
    y = []

    count = 1
    for date in dt_dict[state]:
        x.append(count)
        count += 1
        
        y.append(dt_dict[state][date])
    
    print(x, y)

    fig, ax = plt.subplots(1, 1, figsize=(20, 10), dpi=80)

    for index, value in enumerate(x):    
        if y[index] == 0:
            continue
        else: 
            ax.text(value +dx, y[index] + dy, y[index])


    ax.set_ylabel("Quantidade de {0}".format(item))
    ax.bar(x, y, color=color, tick_label=list( dt_dict[state].keys() ))
    
    plt.title("Quantidade de {0} compradas por {1}".format(item, state))
    plt.xticks(x)

    plt.show()

def barh_x_state_y_total_price(dt_list: list, item: str, color: str="blue", dx = -0.4, dy=10):
    x = list(map(lambda x : x + 1, range(len(dt_list))))
    y = list(map(lambda x : x[1], dt_list))

    fig, ax = plt.subplots(1, 1, figsize=(20, 10), dpi=80)

    for index, value in enumerate(x):    
        if y[index] == 0:
            continue
        else: 
            ax.text( y[index] + dy, value + dx, str(round(y[index], 2)))


    ax.set_ylabel("Quantidade de {0}".format(item))
    ax.barh(x, y, color=color, tick_label=list(map(lambda x : acronym_dict[x[0]] , dt_list)))
    
    plt.title("Valor total gasto por estados em {0}".format(item))
    

    plt.show()

def get_percentage(d: dict ):
    dn = {}
    for k, v in d.items():
        t = v[0] + v[1]

        p1 = v[0] / t * 100

        p2 = v[1] / t * 100
        dn[k] = [p1, p2]
    
    return dn

def pie_vent_types(dt_dict: dict, ufs: list, x=1, y=1):

    fig, ax = plt.subplots(x, y, figsize=(20, 10), dpi=80)

    l = lambda x : str(round(x, 2)) + "%"

    dt_dict = get_percentage(dt_dict)
    index = 0
    for i in range(x):
        for j in range(y):
            if x == 1:
                if y == 1:
                    ax.set_xlabel("Tipos de Respiradores comprados em {0}".format(ufs[index]))
                    patches, texts = ax.pie(dt_dict[ufs[index]], labels = list(map(l, dt_dict[ufs[index]])))
                    plt.legend(patches, ["UTI", "Transporte"], loc="best")
                else:
                    ax[j].set_xlabel("Tipos de Respiradores comprados em {0}".format(ufs[index]))
                    patches, texts = ax[j].pie(dt_dict[ufs[index]], labels = list(map(l, dt_dict[ufs[index]])))
                    plt.legend(patches, ["UTI", "Transporte"], loc="best")
            else:
                if y == 1:
                    ax[i].set_xlabel("Tipos de Respiradores comprados em {0}".format(ufs[index]))
                    patches, texts = ax[i].pie(dt_dict[ufs[index]], labels = list(map(l, dt_dict[ufs[index]])))
                    plt.legend(patches, ["UTI", "Transporte"], loc="best")
                else:
                    ax[i][j].set_xlabel("Tipos de Respiradores comprados em {0}".format(ufs[index]))
                    patches, texts = ax[i][j].pie(dt_dict[ufs[index]], labels = list(map(l, dt_dict[ufs[index]])))
                    plt.legend(patches, ["UTI", "Transporte"], loc="best")
            index+=1

    # ax[1].set_ylabel("Quantidade de {0}".format(item))
    # ax[1].set_xlabel("Quantidade de {0}".format(item))
    # ax[1].pie(dt_dict["ACRE"], labels = list(map(lambda x : str(x), dt_dict["ACRE"])))
    
    # plt.title("Valor total gasto por estados em {0}".format(item))
    # plt.xticks(x)

    plt.show()

def total_price_percentage(chloro_list:list, vent_list:list):
    chrolo_uf = list(map(lambda x : x[0], chloro_list))
    vent_uf = list(map(lambda x : x[0], vent_list))

    total_ptg_list = []

    for uf in acronym_dict.keys():

        chloro = 0
        vent = 0

        if uf in chrolo_uf:
           chloro += chloro_list[chrolo_uf.index(uf)][1]
        
        if uf in vent_uf:
           vent += vent_list[vent_uf.index(uf)][1]
        
        total = vent + chloro

        p1 = chloro / total * 100

        p2 = vent / total * 100

        total_ptg_list.append((uf, p1, p2, chloro, vent, total))
    
    return total_ptg_list


if __name__ == "__main__":
    # chloro_dict = extract_per_state_per_month_csv("./results/chloroquine-per-state-per-month.csv")
    # bar_x_state_y_date(chloro_dict, "Cloroquina", "2020-04", dy=600)
    # bar_x_state_y_date(chloro_dict, "Cloroquina", "2020-07", dy=600)
    # bar_x_state_y_date(chloro_dict, "Cloroquina", "2020-12", dy=300)

    # bar_x_date_y_state(chloro_dict, "Cloroquina", "SÃO PAULO",dx=-0.1, dy=10)
    # bar_x_date_y_state(chloro_dict, "Cloroquina", "RIO DE JANEIRO", dx=-0.1, dy=10)
    # bar_x_date_y_state(chloro_dict, "Cloroquina", "MINAS GERAIS", dx=-0.1, dy=10)

    

    # vent_dict = extract_per_state_per_month_csv("./results/ventilator-per-state-per-month.csv")
    # bar_x_state_y_date(vent_dict, "Respiradores", "2020-04",color="orange", dy=600)
    # bar_x_state_y_date(vent_dict, "Respiradores", "2020-07",color="orange", dy=600)
    # bar_x_state_y_date(vent_dict, "Respiradores", "2020-12", color="orange",dy=300)

    # bar_x_date_y_state(vent_dict, "Respiradores", "SÃO PAULO", color="orange",dx=-0.1, dy=10)
    # bar_x_date_y_state(vent_dict, "Respiradores", "RIO DE JANEIRO", color="orange",dx=-0.1, dy=10)
    # bar_x_date_y_state(vent_dict, "Respiradores", "MINAS GERAIS", color="orange",dx=-0.1, dy=10)




    # vent_list = extract_total_price_per_state_csv("./results/ventilator-total-price-per-state.csv")
    # barh_x_state_y_total_price(vent_list, "respirador", color="orange")

    # chloro_list = extract_total_price_per_state_csv("./results/chloroquine-total-price-per-state.csv")
    # barh_x_state_y_total_price(chloro_list, "cloroquina" )




    # vent_list = extract_total_price_per_state_per_pop_csv("./results/ventilator-total-price-per-state-population.csv")
    # barh_x_state_y_total_price(vent_list, "respirador ( a cada 100 habitantes )", color="orange")

    # chloro_list = extract_total_price_per_state_per_pop_csv("./results/chloroquine-total-price-per-state-population.csv")
    # barh_x_state_y_total_price(chloro_list, "cloroquina ( a cada 100 habitantes )", dy=1)




    dt_dict = extract_vent_types_per_state_csv("./results/ventilator-type-per-state.csv")
    pie_vent_types(dt_dict, ["RIO DE JANEIRO"])
    pie_vent_types(dt_dict, ["SÃO PAULO"])
    pie_vent_types(dt_dict, ["MINAS GERAIS"])
    pie_vent_types(dt_dict, ["RIO GRANDE DO SUL"])
    # pie_vent_types(dt_dict, ["BAHIA", "ACRE", "MINAS GERAIS", "PARÁ"], 2, 2)