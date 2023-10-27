#!/usr/bin/env python3 
##
"""
Script criado para gerar vários arquivos .HTML para serem usados como assinatura de e-mail, seguindo código HTML base e lendo os dados da empresa e funcionários de um arquivo .JSON
As assinaturas serão salvas na pasta definida na váriavel "signature_folder", no mesmo local deste script.

"""

import os
import json
import unicodedata

JSON_data = "dados.json"
HTML_base = "template.html"
signature_folder = "signature"

if not (os.path.exists(JSON_data) and os.path.exists(HTML_base)):
    print("Arquivo JSON de dados dos funcionários ou arquivo HTML de modelo de email não encontrado.")
    print(f"Verifique os arquivos necessários: \n\n	{JSON_data} \n	{HTML_base} \n\n")
    exit(1)  


# Function to remove special characters and accents from the name
def remove_special_characters(name):
    nome_sem_acentos = ''.join(c for c in unicodedata.normalize('NFD', name) if unicodedata.category(c) != 'Mn')
    return ''.join(e for e in nome_sem_acentos if (e.isalnum() or e.isspace()))

# Read data from a JSON file
with open(JSON_data, 'r') as file:
    data = json.load(file)

# Obter informações comuns
common_info = data.get('common_info', {})

# Obter dados dos funcionários
employees = data.get('employees', [])

# Criar a pasta "signature" se ela não existir
if not os.path.exists(signature_folder):
    os.makedirs(signature_folder)

# Read the email template from a file
with open(HTML_base, 'r') as template_file:
    email_template = template_file.read()

for employee in employees:
    # Combinar as informações comuns com os dados do funcionário
    employee_data = {**common_info, **employee}

    # Adjust the name to capitalize (first letter uppercase)
    formatted_name = employee_data["name"].title()
    employee_data["name"] = formatted_name

    # Adjust the title (position) to have only the first letter in lowercase
    formatted_title = employee_data["title"].capitalize()
    employee_data["title"] = formatted_title

    # Remove special characters and accents from the employee name for use in the file name
    file_name = remove_special_characters(formatted_name)

    # Define o nome do arquivo em minúsculo; usar title() para capitalize para ter primeira letra maiúscula)
    file_name = f'{file_name.lower().replace(" ", "_")}.html'  # _signature.html'
    
    # Define o caminho para salvar a assinatura
    file_path = os.path.join(signature_folder, file_name)

    # Replace placeholders in the template with employee-specific data
    email_html = email_template
    for key, value in employee_data.items():
        email_html = email_html.replace(f'{{{{{key}}}}}', value)

    # Save the HTML content to a file in the "signature" folder
    with open(file_path, 'w') as signature_file:
        signature_file.write(email_html)

total_employees = len(employees)
print(f"Funcionários encontrados: {total_employees}")
print(f"Assinaturas em HTML salvas na pasta: {signature_folder} \n")
