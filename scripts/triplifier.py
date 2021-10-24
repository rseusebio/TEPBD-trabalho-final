import sys
from datetime import datetime

# Utilidades 
uf_dbpedia_dict = {
    "SANTA CATARINA": "http://dbpedia.org/resource/Santa_Catarina_(state)",
    "RIO GRANDE DO SUL": "http://dbpedia.org/resource/Rio_Grande_do_Sul",
    "PARANÁ": "http://dbpedia.org/resource/Paraná_(state)",
    "MATO GROSSO": "http://dbpedia.org/resource/Mato_Grosso",
    "MINAS GERAIS": "http://dbpedia.org/resource/Minas_Gerais",
    "GOIÁS": "http://dbpedia.org/resource/Goiás",
    "BAHIA": "http://dbpedia.org/resource/Bahia",
    "ALAGOAS": "http://dbpedia.org/resource/Alagoas",
    "ACRE": "http://dbpedia.org/resource/Acre",
    "AMAPÁ": "http://dbpedia.org/resource/Amapá",
    "AMAZONAS": "http://dbpedia.org/resource/Amazonas",
    "CEARÁ": "http://dbpedia.org/resource/Ceara",
    "DISTRITO FEDERAL": "http://dbpedia.org/resource/Federal_District_(Brazil)",
    "ESPÍRITO SANTO": "http://dbpedia.org/resource/Espírito_Santo",
    "MARANHÃO": "http://dbpedia.org/resource/Maranhão",
    "MATO GROSSO DO SUL": "http://dbpedia.org/resource/Mato_Grosso_do_Sul",
    "PARÁ": "http://dbpedia.org/resource/Pará",
    "PARAÍBA": "http://dbpedia.org/resource/Paraíba",
    "PERNAMBUCO": "http://dbpedia.org/resource/Pernambuco",
    "PIAUÍ": "http://dbpedia.org/resource/Piauí",
    "RIO DE JANEIRO": "http://dbpedia.org/resource/Rio_de_Janeiro_(state)",
    "RIO GRANDE DO NORTE": "http://dbpedia.org/resource/Rio_Grande_do_Norte",
    "RONDÔNIA": "http://dbpedia.org/resource/Rondonia",
    "RORAIMA": "http://dbpedia.org/resource/Roraima",
    "SÃO PAULO": "http://dbpedia.org/resource/São_Paulo_(state)",
    "SERGIPE": "http://dbpedia.org/resource/Sergipe",
    "TOCANTINS": "http://dbpedia.org/resource/Tocantins"
}

def format_date(date: str) -> str:
    try:
        return datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d")

    except Exception as err:
        print("Error:", date, err)

        err.with_traceback()

def format_uf_uri(uri: str) -> str:
    arr = uri.split("/")

    return "dbpg:" + arr[len(arr) - 1]

def format_UF_names(UF: str) -> str:
    if "GOIAS" in UF:
        return "GOIÁS"

    elif "PARANA" in UF:
        return "PARANÁ"

    elif "AMAPA" in UF:
        return "AMAPÁ"
    
    elif "CEARA" in UF:
        return "CEARÁ"
    
    elif "PARA" in UF:
        return "PARÁ"
    
    elif "PARAIBA" in UF:
        return "PARAÍBA"
    
    elif "PIAUI" in UF:
        return "PIAUÍ"
    
    elif "RONDONIA" in UF:
        return "RONDÔNIA"

    elif "ESPIRITO SANTO" in UF:
        return "ESPÍRITO SANTO"
    
    elif "MARANH" in UF:
        return "MARANHÃO"

    elif "PAULO" in UF:
        return "SÃO PAULO"
    
    else:
        return UF

# Chloroquine File
def extract_chloroquine_file(csv_file: str, delimiter: str) -> dict:
    uf_dict = {}

    with open(csv_file, "r", encoding="latin1") as f:
        count_lines = 0

        while True:
            line = f.readline()

            count_lines += 1

            if count_lines == 1:
                continue

            if not line:
                break
            
            if count_lines % 100 == 0:
                print("Reading line {0}".format(count_lines))

            
            arr = line.split(delimiter)

            uf = arr[1].strip()
            program = arr[5].strip()
            qnt = arr[6].strip()
            status = arr[7].strip()
            date = arr[8].strip()
            price = arr[10].replace("R$", "").replace("-", "").replace(".", "").replace(",", ".").strip()

            qnt = abs(int(qnt.replace(".", "").replace(",", "")))

            
            if not price:
                price = qnt * 3
            else:
                price = abs(float(price))

            if program != "COVID-19" or status != "ENTREGA REALIZADA":
                continue 
        
            
            if uf not in uf_dict:
                uf_dict[uf] = {}
            
            if date not in uf_dict[uf]:
                uf_dict[uf][date] = {
                    "qnt": 0,
                    "price": 0
                }
            
            uf_dict[uf][date]["qnt"] += qnt
            uf_dict[uf][date]["price"] += price
    
    return uf_dict 

def transform_chloroquine_in_ttl(output_file: str, uf_dict: dict):
    prefixes = [
        "@prefix : <http://example.com/> .\n",
        "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n",
        "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n",
        "@prefix foaf: <http://xmlns.com/foaf/0.1/> .\n",
        "@prefix dbo: <http://dbpedia.org/ontology/> .\n",
        "@prefix dbr: <http://dbpedia.org/resouce/> .\n",
        "@prefix dbp: <http://dbpedia.org/property/> .\n",
        "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n",
        "@prefix owl: <http://www.w3.org/2002/07/owl#> .\n",
        "@prefix wiki-en: <http://en.wikipedia.org/wiki/> .\n\n",
    ]
    
    with open(output_file, "w") as f:
        f.writelines(prefixes)

        product_id = 1

        for uf, dict in uf_dict.items():
            f.write("<{0}>  rdf:name \"{1}\"@pt .\n\n".format(uf_dbpedia_dict[uf], uf))
            
            for date, value in dict.items():

                qnt = value["qnt"]
                price = value["price"]

                lines = [
                    ":chloroquine_{0} rdf:type dbo:drug ;\n".format(product_id),
                    "                 rdfs:label \"chloroquine\"^^xsd:string ;\n",
                    "                 rdf:isPrimaryTopicOf wiki-en:Chloroquine ;\n",
                    "                 owl:sameAs dbr:Chloroquine ;\n",
                    "                 dbp:amount \"{0}\"^^xsd:integer ;\n".format(qnt),
                    "                 dbo:price \"{0}\"^^xsd:double ;\n".format(price),
                    "                 dbo:date \"{0}\"^^xsd:date .\n\n".format(format_date(date)),

                    "<{0}> dbp:order :chloroquine_{1} .\n\n".format(uf_dbpedia_dict[uf], product_id)
                ]

                product_id += 1

                f.writelines(lines)

def get_chloroquine_turtle():
    file_name = "./csv_files/distribuicao_cloroquina.csv"
    uf_dict = extract_chloroquine_file(file_name, ";")

    for uf in uf_dict:
        (uf, uf_dbpedia_dict[uf])

    transform_chloroquine_in_ttl("./ouput_rdf/rdf_dataset_chloroquine.ttl", uf_dict)

    print("\nFinished converting chloroquine dataset.\n")

# Ventilator File
def extract_ventilator_file(csv_file: str, delimiter: str) -> dict:
    uf_dict = {}

    with open(csv_file, "r", encoding="latin1") as f:
        count_lines = 0

        while True:
            line = f.readline()

            count_lines += 1

            if count_lines == 1:
                continue

            elif not line or count_lines >= 2649:
                break
            
            if count_lines % 100 == 0:
                print("Reading line {0}".format(count_lines))
            
            arr = line.split(delimiter)
            
            date = arr[0].strip().split(" ")[0].strip()
            uf = format_UF_names(arr[2].strip())
            vent_type = "Transporte" if "transporte" in arr[4].strip().lower() else "UTI"
            qnt = arr[5].strip()
            price = arr[6].replace("R$", "").replace(".", "").replace(",", ".").strip()

            qnt = abs(int(qnt.replace(".", "").replace(",", "")))
            price = abs(float(price))

            # if count_lines % 100 == 0:
            #     print("line {0}".format(line))
            
            if uf not in uf_dict:
                uf_dict[uf] = {}
            
            if date not in uf_dict[uf]:
                uf_dict[uf][date] = {}
            
            if vent_type not in uf_dict[uf][date]:
                uf_dict[uf][date][vent_type] = {
                    "qnt": 0, 
                    "price": 0
                }
            
            uf_dict[uf][date][vent_type]["qnt"] += qnt
            uf_dict[uf][date][vent_type]["price"] += price
    
    return uf_dict 

def transform_ventilator_in_ttl(output_file: str, uf_dict: dict):
    prefixes = [
        "@prefix : <http://example.com/> .\n",
        "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n",
        "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n",
        "@prefix foaf: <http://xmlns.com/foaf/0.1/> .\n",
        "@prefix dbo: <http://dbpedia.org/ontology/> .\n",
        "@prefix dbr: <http://dbpedia.org/resouce/> .\n",
        "@prefix dbp: <http://dbpedia.org/property/> .\n",
        "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n",
        "@prefix wiki-en: <http://en.wikipedia.org/wiki/> .\n",
        "@prefix owl: <http://www.w3.org/2002/07/owl#> .\n\n"
    ]
    
    with open(output_file, "w") as f:
        f.writelines(prefixes)

        product_id = 1

        for uf, dict in uf_dict.items():
            f.write("<{0}>  rdf:name \"{1}\"@pt .\n\n".format(uf_dbpedia_dict[uf], uf))

            for date, type_dict in dict.items():

                for type, obj in type_dict.items():

                    qnt = obj["qnt"]
                    price = obj["price"]

                    type = "ICU" if "UTI" in type else "Transport"

                    lines = [
                        ":ventilator_{0} rdf:type dbo:Device ;\n".format(product_id),
                        "                 rdfs:label \"{0} Ventilator\"^^xsd:string ;\n".format(type),
                        "                 rdf:isPrimaryTopicOf wiki-en:Ventilator ;\n",
                        "                 owl:sameAs dbr:Ventilator ;\n",
                        "                 dbp:amount \"{0}\"^^xsd:integer ;\n".format(qnt),
                        "                 dbo:date \"{0}\"^^xsd:date ;\n".format(format_date(date)),
                        "                 dbo:price \"{0}\"^^xsd:double .\n\n".format(price),

                        "<{0}> dbp:order :ventilator_{1} .\n\n".format(uf_dbpedia_dict[uf], product_id)                    
                    ]

                    product_id += 1

                    f.writelines(lines)

def get_ventilator_turtle():
    file_name = "./csv_files/distribuicao_respiradores.csv"

    uf_dict = extract_ventilator_file(file_name, ";")

    for uf in uf_dict:
        (uf, uf_dbpedia_dict[uf])

    transform_ventilator_in_ttl("./ouput_rdf/rdf_dataset_ventilator.ttl", uf_dict)

    print("\nFinished converting ventilator dataset.\n")


if __name__ == "__main__":
    get_ventilator_turtle()

    get_chloroquine_turtle()