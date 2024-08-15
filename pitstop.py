import tkinter as tk
from tkinter import messagebox
import requests

# Define the prices for each part
prices_estetica = {
    'Porta': 50,
    'Capô': 50,
    'Mala': 50,
    'Vidro': 50,
    'Parte de Pneu': 60,
    'Kit Avanaçado': 80
}

prices_motor = {
    'Filtro Óleo': 122,
    'Filtro de Ar': 122,
    'Bomba de Combustível': 122,
    'Refrigerante': 100,
    'Fluido Travões': 55,
    'Fluido Direção': 100,
    'Fluido Transmissão': 100,
    'Velas de Ignição': 194,
    'Cintos de Segurança': 28,
    'Volante': 28,
    'Borracha dos Pneus': 29,
    'Radiador': 324,
    'Bomba de Combustivel': 79,
    'Travoes': 60,
    'Eixo de Transmissao': 90,
    'Alternador': 489,
    'Embreagem': 90
}

# Initialize the total repairs of the day
total_repairs_of_day = 0
current_total = 0  # To hold the calculated total before confirmation
fatura_enviada = 0

# Function to calculate the total cost
def calculate_total():
    global current_total
    total_cost = 0
    try:
        for part, entry in estetica_entries.items():
            value = entry.get()
            quantity = int(value) if value.strip() else 0  # Treat empty as 0
            total_cost += quantity * prices_estetica[part]

        for part, entry in motor_entries.items():
            value = entry.get()
            quantity = int(value) if value.strip() else 0  # Treat empty as 0
            total_cost += quantity * prices_motor[part]
        
        current_total = total_cost
        total_label.config(text=f'Total: {total_cost}€')
    except ValueError:
        messagebox.showerror("INVALIDO", "Mete quantias validas")

# Function to confirm and add the current total to the daily total
def confirm_total():
    calculate_total()
    global total_repairs_of_day, current_total
    total_repairs_of_day += current_total
    daily_total_label.config(text=f'Reparações do Dia: {total_repairs_of_day}€')
    current_total = 0
    total_label.config(text=f'Total: {current_total}€')
    clear_inputs()  # Optionally clear inputs after confirming

# Function to clear all input fields
def clear_inputs():
    for entry in estetica_entries.values():
        entry.delete(0, tk.END)
    for entry in motor_entries.values():
        entry.delete(0, tk.END)

# Function to show the "Reparação" page
def show_reparacao():
    if not mecanico_confirmed:
        messagebox.showerror("INVALIDO", "Confirme o nome do mecânico antes de continuar")
        return
    repair_frame.pack(fill="both", expand=True)
    performance_frame.pack_forget()
    insurance_frame.pack_forget()
    search_frame.pack_forget()

# Function to show the "Performance" page
def show_performance():
    if not mecanico_confirmed:
        messagebox.showerror("INVALIDO", "Confirme o nome do mecânico antes de continuar")
        return
    performance_frame.pack(fill="both", expand=True)
    repair_frame.pack_forget()
    insurance_frame.pack_forget()
    search_frame.pack_forget()

# Function to show the "Seguro" page
def show_insurance():
    if not mecanico_confirmed:
        messagebox.showerror("INVALIDO", "Confirme o nome do mecânico antes de continuar")
        return
    insurance_frame.pack(fill="both", expand=True)
    repair_frame.pack_forget()
    performance_frame.pack_forget()
    search_frame.pack_forget()

# Function to show the "Procurar Seguro" page
def show_search():
    if not mecanico_confirmed:
        messagebox.showerror("INVALIDO", "Confirme o nome do mecânico antes de continuar")
        return
    search_frame.pack(fill="both", expand=True)
    repair_frame.pack_forget()
    performance_frame.pack_forget()
    insurance_frame.pack_forget()

# Function to add insurance details to seguros.txt
def add_cliente():
    nome = nome_entry.get().strip()
    nss = nss_entry.get().strip()
    data_inicio = data_inicio_entry.get().strip()
    data_final = data_final_entry.get().strip()
    
    if not nome or not nss or not data_inicio or not data_final:
        messagebox.showerror("INVALIDO", "Todos os campos são obrigatórios")
        return
    
    with open("seguros.txt", "a") as file:
        file.write(f"{nome} | {nss} | {data_inicio} | {data_final}\n")
    
    messagebox.showinfo("SUCESSO", "Cliente adicionado com sucesso")
    nome_entry.delete(0, tk.END)
    nss_entry.delete(0, tk.END)
    data_inicio_entry.delete(0, tk.END)
    data_final_entry.delete(0, tk.END)

# Function to search for insurance details in seguros.txt
def search_cliente():
    search_nome = search_nome_entry.get().strip()
    
    if not search_nome:
        messagebox.showerror("INVALIDO", "O campo Nome é obrigatório")
        return
    
    found = False
    with open("seguros.txt", "r") as file:
        for line in file:
            nome, nss, data_inicio, data_final = line.strip().split(" | ")
            if nome == search_nome:
                search_result_nome.config(text=f"Nome: {nome}")
                search_result_nss.config(text=f"NSS: {nss}")
                search_result_data_inicio.config(text=f"Data Inicio: {data_inicio}")
                search_result_data_final.config(text=f"Data Final: {data_final}")
                found = True
                break
    
    if not found:
        messagebox.showinfo("RESULTADO", "Nome não encontrado")

# Function to send the invoice information to Discord
def send_invoice():
    if not mecanico_confirmed:
        messagebox.showerror("INVALIDO", "Confirme o nome do mecânico antes de continuar")
        return

    mecânico_name = mecanico_name
    if not mecânico_name:
        messagebox.showerror("INVALIDO", "Nome do Mecânico é obrigatório")
        return

    webhook_url = "https://discord.com/api/webhooks/1266114207011569685/tt-ihXpuMG5PHCjHNxAphAT4ulU2HzGWku7Rmepf1LEWC6wIwme3W-PhwMpVdu5oYuwU"  
    message = {
        "content": f"**Faturaçâo**\nMecânico: {mecânico_name}\nTotal Reparações do Dia: {total_repairs_of_day}€"
    }
    try:
        response = requests.post(webhook_url, json=message)
        response.raise_for_status()
        messagebox.showinfo("SUCESSO", "Faturaçâo enviada com sucesso")
        fatura_enviada = 1
    except requests.RequestException as e:
        messagebox.showerror("ERRO", f"Erro ao enviar faturaçâo: {e}")

# Function to send the repair cost to Discord
def send_repair_cost_to_discord(total_cost, bombeiro):
    if not mecanico_confirmed:
        messagebox.showerror("INVALIDO", "Confirme o nome do mecânico antes de continuar")
        return

    webhook_url = "https://discord.com/api/webhooks/1266114207276073065/xflV15mxCbO7Hde_Q1XU4asVmL9dUQTjedDXHpCtBWdrFlWyHbbgyH8T4Aw0K9kDEQRl"  
    message = {
        "content": f"**Faturaçâo**\nReparaçao do bombeiro **{bombeiro}**: {total_cost}€"
    }
    try:
        response = requests.post(webhook_url, json=message)
        response.raise_for_status()
        messagebox.showinfo("SUCESSO", "Custo da reparaçao enviada com sucesso")
    except requests.RequestException as e:
        messagebox.showerror("ERRO", f"Erro ao enviar custo da reparaçao: {e}")

# Function to handle the close event
def on_closing():
    if fatura_enviada == 1:
        root.destroy()
    else:
        if messagebox.askyesno("Confirmação", "Mandas-te a Faturação Total?"):
            root.destroy()

# Function to confirm the mechanic's name
def confirm_mecanico():
    global mecanico_name, mecanico_confirmed
    mecanico_name = mecanico_entry.get().strip()
    if not mecanico_name:
        messagebox.showerror("INVALIDO", "Nome do Mecânico é obrigatório")
        return
    mecanico_confirmed = True
    mecanico_entry.config(state='disabled')
    mecanico_label.config(text=f"Mecânico: {mecanico_name}")

# Function to handle "Conta Mecanico" button click
def conta_mecanico():
    bombeiro = bombeiro_entry.get().strip()
    send_repair_cost_to_discord(current_total,bombeiro)
    confirm_total()

# Create the main window
root = tk.Tk()

root.title("CALCULADORA PITSTOP")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry("1820x980")

root.resizable(True, True)  # Disable window resizing

# Bind the on_closing function to the window's close event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Create a container frame for navigation and content
container = tk.Frame(root)
container.pack(fill="both", expand=True)

# Create frames for the "Reparação", "Performance", "Seguro", and "Procurar Seguro" pages
repair_frame = tk.Frame(container)
performance_frame = tk.Frame(container)
insurance_frame = tk.Frame(container)
search_frame = tk.Frame(container)

# Initialize mechanic name and confirmation state
mecanico_name = ""
mecanico_confirmed = False

# Create the main menu
menu_frame = tk.Frame(container)
menu_frame.pack(fill="both", expand=True)

tk.Label(menu_frame, text="Escolha uma opção", font=('Arial', 16)).pack(pady=10)

tk.Label(menu_frame, text="Nome do Mecânico", font=('Arial', 14)).pack(pady=5)
mecanico_entry = tk.Entry(menu_frame, width=20)
mecanico_entry.pack(pady=5)

confirm_mecanico_button = tk.Button(menu_frame, text="Confirmar Mecânico", command=confirm_mecanico)
confirm_mecanico_button.pack(pady=5)

repair_button = tk.Button(menu_frame, text="Reparação", command=show_reparacao)
repair_button.pack(pady=5)

performance_button = tk.Button(menu_frame, text="Performance", command=show_performance)
performance_button.pack(pady=5)

insurance_button = tk.Button(menu_frame, text="Adicionar Seguro", command=show_insurance)
insurance_button.pack(pady=5)

search_button = tk.Button(menu_frame, text="Procurar Seguro", command=show_search)
search_button.pack(pady=5)

# Label to display the mechanic's name
mecanico_label = tk.Label(root, text="", font=('Arial', 14))
mecanico_label.pack(anchor='ne', padx=10, pady=10)

# Create the "Reparação" page content
repair_content = tk.Frame(repair_frame)
repair_content.pack(expand=True)

tk.Label(repair_content, text="Estética", font=('Arial', 14)).grid(row=0, column=0, columnspan=2, pady=(10, 0))
estetica_entries = {}
for i, part in enumerate(prices_estetica.keys()):
    tk.Label(repair_content, text=part).grid(row=i+1, column=0, sticky='e')
    entry = tk.Entry(repair_content, width=5)
    entry.grid(row=i+1, column=1)
    estetica_entries[part] = entry

tk.Label(repair_content, text="Motor", font=('Arial', 14)).grid(row=0, column=2, columnspan=2, pady=(10, 0))
motor_entries = {}
for i, part in enumerate(prices_motor.keys()):
    tk.Label(repair_content, text=part).grid(row=i+1, column=2, sticky='e')
    entry = tk.Entry(repair_content, width=5)
    entry.grid(row=i+1, column=3)
    motor_entries[part] = entry
    
tk.Label(repair_content, text="Em Caso de Bombeiro", font=('Arial', 14)).grid(row=0, column=4, columnspan=2, pady=(10, 0))
tk.Label(repair_content, text="Bombeiro").grid(row=1, column=4, sticky='e')
bombeiro_entry = tk.Entry(repair_content, width=20)
bombeiro_entry.grid(row=1, column=5)


calculate_button = tk.Button(repair_content, text="Calcular", command=calculate_total)
calculate_button.grid(row=max(len(prices_estetica), len(prices_motor))+1, column=2, columnspan=1, pady=10)

confirm_button = tk.Button(repair_content, text="Confirmar", command=confirm_total)
confirm_button.grid(row=max(len(prices_estetica), len(prices_motor))+1, column=3, columnspan=1, pady=10)

clear_button = tk.Button(repair_content, text="Nova Reparação", command=clear_inputs)
clear_button.grid(row=max(len(prices_estetica), len(prices_motor))+1, column=0, columnspan=2, pady=10)

send_invoice_button = tk.Button(repair_content, text="Enviar Faturação", command=send_invoice)
send_invoice_button.grid(row=max(len(prices_estetica), len(prices_motor))+1, column=4, columnspan=2, pady=10)

# New "Conta Mecanico" button
conta_mecanico_button = tk.Button(repair_content, text="Conta Bombeiro", command=conta_mecanico)
conta_mecanico_button.grid(row=max(len(prices_estetica), len(prices_motor))+2, column=2, columnspan=2, pady=10)

total_label = tk.Label(repair_content, text="Total: 0€", font=('Arial', 14))
total_label.grid(row=max(len(prices_estetica), len(prices_motor))+3, column=0, columnspan=4, pady=10)

daily_total_label = tk.Label(repair_content, text="Reparações do Dia: 0€", font=('Arial', 14))
daily_total_label.grid(row=max(len(prices_estetica), len(prices_motor))+4, column=0, columnspan=4, pady=10)

# Create the "Performance" page content (currently just a placeholder)
tk.Label(performance_frame, text="Página de Performance em desenvolvimento", font=('Arial', 16)).pack(pady=20)

# Create the "Seguro" page content
insurance_content = tk.Frame(insurance_frame)
insurance_content.pack(expand=True)

tk.Label(insurance_content, text="Nome", font=('Arial', 14)).grid(row=0, column=0, sticky='e', padx=5, pady=5)
nome_entry = tk.Entry(insurance_content, width=20)
nome_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(insurance_content, text="NSS", font=('Arial', 14)).grid(row=1, column=0, sticky='e', padx=5, pady=5)
nss_entry = tk.Entry(insurance_content, width=20)
nss_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(insurance_content, text="Data Inicio", font=('Arial', 14)).grid(row=2, column=0, sticky='e', padx=5, pady=5)
data_inicio_entry = tk.Entry(insurance_content, width=20)
data_inicio_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(insurance_content, text="Data Final", font=('Arial', 14)).grid(row=3, column=0, sticky='e', padx=5, pady=5)
data_final_entry = tk.Entry(insurance_content, width=20)
data_final_entry.grid(row=3, column=1, padx=5, pady=5)

add_cliente_button = tk.Button(insurance_content, text="Adicionar Cliente", command=add_cliente)
add_cliente_button.grid(row=4, column=0, columnspan=2, pady=10)

# Create the "Procurar Seguro" page content
search_content = tk.Frame(search_frame)
search_content.pack(expand=True)

tk.Label(search_content, text="Procurar Seguro", font=('Arial', 16)).pack(pady=10)

tk.Label(search_content, text="Nome", font=('Arial', 14)).pack(pady=5)
search_nome_entry = tk.Entry(search_content, width=20)
search_nome_entry.pack(pady=5)

search_button = tk.Button(search_content, text="Procurar", command=search_cliente)
search_button.pack(pady=10)

search_result_nome = tk.Label(search_content, text="Nome: ", font=('Arial', 14))
search_result_nome.pack(pady=5)

search_result_nss = tk.Label(search_content, text="NSS: ", font=('Arial', 14))
search_result_nss.pack(pady=5)

search_result_data_inicio = tk.Label(search_content, text="Data Inicio: ", font=('Arial', 14))
search_result_data_inicio.pack(pady=5)

search_result_data_final = tk.Label(search_content, text="Data Final: ", font=('Arial', 14))
search_result_data_final.pack(pady=5)

# Initially show the menu page
menu_frame.pack(fill="both", expand=True)

# Run the application
root.mainloop()
