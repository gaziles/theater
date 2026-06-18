from tkinter import *
from tkinter import ttk
import tkintermapview
from PIL import Image, ImageDraw, ImageFont
import io
import time
from theater_lib.model import theaters
from theater_lib.controller import *

# ========== STYL ==========

BG         = "#F7F8FA"
PANEL_BG   = "#FFFFFF"
ACCENT     = "#4F6CF7"
ACCENT2    = "#6EE7B7"
DANGER     = "#F87171"
TEXT       = "#1E293B"
SUBTEXT    = "#64748B"
BORDER     = "#E2E8F0"
BTN_FG     = "#FFFFFF"
FONT       = "Segoe UI"

def style_button(btn, color=ACCENT, fg=BTN_FG):
    btn.config(
        bg=color, fg=fg,
        font=(FONT, 9, "bold"),
        relief=FLAT,
        bd=0,
        padx=10, pady=4,
        cursor="hand2",
        activebackground=color,
        activeforeground=fg,
    )

def style_entry(e):
    e.config(
        font=(FONT, 9),
        relief=FLAT,
        bd=1,
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=ACCENT,
        bg="#F1F5F9",
        fg=TEXT,
        insertbackground=ACCENT,
    )

def style_listbox(lb):
    lb.config(
        font=(FONT, 9),
        bg=PANEL_BG,
        fg=TEXT,
        selectbackground=ACCENT,
        selectforeground=BTN_FG,
        relief=FLAT,
        bd=0,
        highlightthickness=1,
        highlightbackground=BORDER,
    )

def style_label(lbl, bold=False, sub=False):
    color = SUBTEXT if sub else TEXT
    weight = "bold" if bold else "normal"
    lbl.config(font=(FONT, 9, weight), bg=PANEL_BG, fg=color)

def style_section_label(lbl):
    lbl.config(font=(FONT, 11, "bold"), bg=BG, fg=ACCENT)

def make_panel(parent):
    f = Frame(parent, bg=PANEL_BG, bd=0, relief=FLAT,
              highlightthickness=1, highlightbackground=BORDER)
    return f

# ========== GŁÓWNE OKNO ==========

root = Tk()
root.title("System Zarządzania Teatrami")
root.geometry("1200x800")
root.config(bg=BG)

style = ttk.Style()
style.theme_use("clam")
style.configure("TNotebook", background=BG, borderwidth=0)
style.configure("TNotebook.Tab",
    font=(FONT, 10, "bold"),
    padding=[16, 6],
    background=BORDER,
    foreground=SUBTEXT,
)
style.map("TNotebook.Tab",
    background=[("selected", PANEL_BG)],
    foreground=[("selected", ACCENT)],
)
style.configure("TFrame", background=BG)

notebook = ttk.Notebook(root)

tab_theaters  = Frame(notebook, bg=BG)
tab_clients   = Frame(notebook, bg=BG)
tab_employees = Frame(notebook, bg=BG)
tab_views     = Frame(notebook, bg=BG)

notebook.add(tab_theaters,  text="  Teatry  ")
notebook.add(tab_clients,   text="  Klienci  ")
notebook.add(tab_employees, text="  Pracownicy  ")
notebook.add(tab_views,     text="  Wyszukiwarka  ")

notebook.pack(fill=BOTH, expand=True, padx=8, pady=8)

# Płaskie listy z przypisanym teatrem
clients = []
for t in theaters:
    for c in t.get("clients", []):
        c.setdefault("theater", t["name"])
        c.setdefault("marker", None)
        clients.append(c)

employees = []
for t in theaters:
    for e in t.get("employees", []):
        e.setdefault("theater", t["name"])
        e.setdefault("marker", None)
        employees.append(e)

for t in theaters:
    t.setdefault("marker", None)


# ========== MARKERY ==========

def make_circle_marker(color, size=28):
    from PIL import ImageTk
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([2, 2, size - 2, size - 2], fill=color, outline="white", width=2)
    tk_img = ImageTk.PhotoImage(img)
    # Przechowaj referencję na root, żeby GC nie usunął obrazka
    if not hasattr(root, "_icon_refs"):
        root._icon_refs = []
    root._icon_refs.append(tk_img)
    return tk_img

icon_theater  = None
icon_client   = None
icon_employee = None

def init_icons():
    global icon_theater, icon_client, icon_employee
    icon_theater  = make_circle_marker("#4F6CF7")
    icon_client   = make_circle_marker("#6EE7B7")
    icon_employee = make_circle_marker("#F87171")

def set_marker(map_widget, coords, text, icon):
    return map_widget.set_marker(
        coords[0], coords[1],
        text=text,
        icon=icon,
        icon_anchor="center",
        font=(FONT, 10, "bold"),
        text_color=TEXT
    )


# ========== TEATRY ==========

frame_theater_list    = make_panel(tab_theaters)
frame_theater_form    = make_panel(tab_theaters)
frame_theater_details = make_panel(tab_theaters)
frame_theater_map     = Frame(tab_theaters, bg=BG)

frame_theater_list.grid(   row=0, column=0, padx=10, pady=10, sticky=N)
frame_theater_form.grid(   row=0, column=1, padx=10, pady=10, sticky=N)
frame_theater_details.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky=EW)
frame_theater_map.grid(    row=0, column=2, rowspan=2, padx=10, pady=10)

# Lista
lbl = Label(frame_theater_list, text="Lista teatrów")
style_section_label(lbl); lbl.grid(row=0, column=0, columnspan=2, pady=(10,6), padx=10)

entry_theater_filter = Entry(frame_theater_list)
style_entry(entry_theater_filter)
entry_theater_filter.grid(row=1, column=0, padx=(10,4), pady=4)

btn_search_t = Button(frame_theater_list, text="Szukaj", command=lambda: filter_theaters())
style_button(btn_search_t)
btn_search_t.grid(row=1, column=1, padx=(0,10), pady=4)

listbox_theaters = Listbox(frame_theater_list, width=30, height=10)
style_listbox(listbox_theaters)
listbox_theaters.grid(row=2, column=0, columnspan=2, padx=10, pady=4)

btn_details_t = Button(frame_theater_list, text="Szczegóły", command=lambda: show_theater_details())
style_button(btn_details_t, ACCENT)
btn_details_t.grid(row=3, column=0, padx=(10,4), pady=4)

btn_edit_t = Button(frame_theater_list, text="Edytuj", command=lambda: edit_theater_gui())
style_button(btn_edit_t, SUBTEXT)
btn_edit_t.grid(row=3, column=1, padx=(0,10), pady=4)

btn_del_t = Button(frame_theater_list, text="Usuń", command=lambda: delete_theater_gui())
style_button(btn_del_t, DANGER)
btn_del_t.grid(row=4, column=0, columnspan=2, padx=10, pady=(2,10))

# Formularz
lbl2 = Label(frame_theater_form, text="Nowy teatr")
style_section_label(lbl2); lbl2.grid(row=0, column=0, columnspan=2, pady=(10,6), padx=10)

for row, text in [(1, "Nazwa:"), (2, "Lokalizacja:")]:
    l = Label(frame_theater_form, text=text)
    style_label(l, sub=True)
    l.grid(row=row, column=0, sticky=W, padx=(10,4), pady=3)

entry_theater_name     = Entry(frame_theater_form)
entry_theater_location = Entry(frame_theater_form)
for row, e in [(1, entry_theater_name), (2, entry_theater_location)]:
    style_entry(e)
    e.grid(row=row, column=1, padx=(0,10), pady=3)

button_add_theater = Button(frame_theater_form, text="Dodaj teatr", command=lambda: add_theater_gui())
style_button(button_add_theater)
button_add_theater.grid(row=3, column=0, columnspan=2, pady=(6,12), padx=10)

# Szczegóły
frame_theater_details.config(bg=PANEL_BG)
lbl3 = Label(frame_theater_details, text="Szczegóły")
style_section_label(lbl3); lbl3.grid(row=0, column=0, columnspan=4, pady=(8,4), padx=10, sticky=W)

for col, text in [(0,"Nazwa:"), (2,"Lokalizacja:")]:
    l = Label(frame_theater_details, text=text)
    style_label(l, sub=True)
    l.grid(row=1, column=col, sticky=W, padx=(10,2))

label_theater_name_val = Label(frame_theater_details, text="—")
style_label(label_theater_name_val, bold=True)
label_theater_name_val.grid(row=1, column=1, sticky=W, padx=(0,20))

label_theater_location_val = Label(frame_theater_details, text="—")
style_label(label_theater_location_val, bold=True)
label_theater_location_val.grid(row=1, column=3, sticky=W, padx=(0,10), pady=(0,8))

map_theaters = tkintermapview.TkinterMapView(frame_theater_map, width=500, height=400)
map_theaters.set_position(52.2, 21.0)
map_theaters.set_zoom(6)
map_theaters.grid(row=0, column=0)


def refresh_theaters():
    listbox_theaters.delete(0, END)
    for t in theaters:
        listbox_theaters.insert(END, t["name"])

def show_theater_details():
    i = listbox_theaters.curselection()
    if not i: return
    t = theaters[i[0]]
    label_theater_name_val.config(text=t["name"])
    label_theater_location_val.config(text=t["location"])
    coords = get_coordinates(t["location"])
    if coords:
        map_theaters.set_position(coords[0], coords[1])
        map_theaters.set_zoom(12)

def add_theater_gui():
    name     = entry_theater_name.get()
    location = entry_theater_location.get()
    if not name or not location: return
    new = {"name": name, "location": location, "clients": [], "employees": [], "marker": None}
    theaters.append(new)
    try:
        coords = get_coordinates(location)
        if coords:
            new["marker"] = set_marker(map_theaters, coords, name, icon_theater)
    except: pass
    entry_theater_name.delete(0, END)
    entry_theater_location.delete(0, END)
    refresh_theaters()

def edit_theater_gui():
    i = listbox_theaters.curselection()
    if not i: return
    t = theaters[i[0]]
    entry_theater_name.delete(0, END)
    entry_theater_location.delete(0, END)
    entry_theater_name.insert(0, t["name"])
    entry_theater_location.insert(0, t["location"])
    style_button(button_add_theater, ACCENT2, TEXT)
    button_add_theater.config(text="Zapisz zmiany", command=lambda idx=i[0]: save_theater(idx))

def save_theater(i):
    t = theaters[i]
    if t["marker"]: t["marker"].delete()
    t["name"]     = entry_theater_name.get()
    t["location"] = entry_theater_location.get()
    try:
        coords = get_coordinates(t["location"])
        if coords:
            t["marker"] = set_marker(map_theaters, coords, t["name"], icon_theater)
    except: pass
    entry_theater_name.delete(0, END)
    entry_theater_location.delete(0, END)
    style_button(button_add_theater)
    button_add_theater.config(text="Dodaj teatr", command=lambda: add_theater_gui())
    refresh_theaters()

def delete_theater_gui():
    i = listbox_theaters.curselection()
    if not i: return
    t = theaters[i[0]]
    if t["marker"]: t["marker"].delete()
    theaters.pop(i[0])
    refresh_theaters()

def filter_theaters():
    search = entry_theater_filter.get().lower()
    listbox_theaters.delete(0, END)
    for t in theaters:
        if search in t["name"].lower() or search in t["location"].lower():
            listbox_theaters.insert(END, t["name"])

def load_theater_markers():
    for t in theaters:
        try:
            coords = get_coordinates(t["location"])
            if coords:
                t["marker"] = set_marker(map_theaters, coords, t["name"], icon_theater)
            time.sleep(1.1)
        except: pass

refresh_theaters()


# ========== KLIENCI ==========

frame_client_list    = make_panel(tab_clients)
frame_client_form    = make_panel(tab_clients)
frame_client_details = make_panel(tab_clients)
frame_client_map     = Frame(tab_clients, bg=BG)

frame_client_list.grid(   row=0, column=0, padx=10, pady=10, sticky=N)
frame_client_form.grid(   row=0, column=1, padx=10, pady=10, sticky=N)
frame_client_details.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky=EW)
frame_client_map.grid(    row=0, column=2, rowspan=2, padx=10, pady=10)

lbl = Label(frame_client_list, text="Lista klientów")
style_section_label(lbl); lbl.grid(row=0, column=0, columnspan=2, pady=(10,6), padx=10)

entry_client_filter = Entry(frame_client_list)
style_entry(entry_client_filter)
entry_client_filter.grid(row=1, column=0, padx=(10,4), pady=4)

btn_sc = Button(frame_client_list, text="Szukaj", command=lambda: filter_clients())
style_button(btn_sc)
btn_sc.grid(row=1, column=1, padx=(0,10), pady=4)

listbox_clients = Listbox(frame_client_list, width=30, height=10)
style_listbox(listbox_clients)
listbox_clients.grid(row=2, column=0, columnspan=2, padx=10, pady=4)

btn_dc = Button(frame_client_list, text="Szczegóły", command=lambda: show_client_details())
style_button(btn_dc, ACCENT)
btn_dc.grid(row=3, column=0, padx=(10,4), pady=4)

btn_ec = Button(frame_client_list, text="Edytuj", command=lambda: edit_client_gui())
style_button(btn_ec, SUBTEXT)
btn_ec.grid(row=3, column=1, padx=(0,10), pady=4)

btn_delc = Button(frame_client_list, text="Usuń", command=lambda: delete_client_gui())
style_button(btn_delc, DANGER)
btn_delc.grid(row=4, column=0, columnspan=2, padx=10, pady=(2,10))

lbl2 = Label(frame_client_form, text="Nowy klient")
style_section_label(lbl2); lbl2.grid(row=0, column=0, columnspan=2, pady=(10,6), padx=10)

field_labels = ["Imię i nazwisko:", "Lokalizacja:", "Teatr:", "Spektakle (po przecinku):"]
for row, text in enumerate(field_labels, start=1):
    l = Label(frame_client_form, text=text)
    style_label(l, sub=True)
    l.grid(row=row, column=0, sticky=W, padx=(10,4), pady=3)

entry_client_name         = Entry(frame_client_form)
entry_client_location     = Entry(frame_client_form)
entry_client_theater      = Entry(frame_client_form)
entry_client_performances = Entry(frame_client_form)
for row, e in enumerate([entry_client_name, entry_client_location,
                          entry_client_theater, entry_client_performances], start=1):
    style_entry(e)
    e.grid(row=row, column=1, padx=(0,10), pady=3)

button_add_client = Button(frame_client_form, text="Dodaj klienta", command=lambda: add_client_gui())
style_button(button_add_client)
button_add_client.grid(row=5, column=0, columnspan=2, pady=(6,12), padx=10)

frame_client_details.config(bg=PANEL_BG)
lbl3 = Label(frame_client_details, text="Szczegóły")
style_section_label(lbl3); lbl3.grid(row=0, column=0, columnspan=8, pady=(8,4), padx=10, sticky=W)

detail_labels = ["Nazwa:", "Lokalizacja:", "Teatr:", "Spektakle:"]
for col_idx, text in enumerate(detail_labels):
    l = Label(frame_client_details, text=text)
    style_label(l, sub=True)
    l.grid(row=1, column=col_idx*2, sticky=W, padx=(10,2))

label_client_name_val         = Label(frame_client_details, text="—"); style_label(label_client_name_val, bold=True)
label_client_location_val     = Label(frame_client_details, text="—"); style_label(label_client_location_val, bold=True)
label_client_theater_val      = Label(frame_client_details, text="—"); style_label(label_client_theater_val, bold=True)
label_client_performances_val = Label(frame_client_details, text="—"); style_label(label_client_performances_val, bold=True)

for col_idx, lbl in enumerate([label_client_name_val, label_client_location_val,
                                label_client_theater_val, label_client_performances_val]):
    lbl.grid(row=1, column=col_idx*2+1, sticky=W, padx=(0,16), pady=(0,8))

map_clients = tkintermapview.TkinterMapView(frame_client_map, width=500, height=400)
map_clients.set_position(52.2, 21.0)
map_clients.set_zoom(6)
map_clients.grid(row=0, column=0)


def refresh_clients():
    listbox_clients.delete(0, END)
    for c in clients:
        listbox_clients.insert(END, c["name"])

def show_client_details():
    i = listbox_clients.curselection()
    if not i: return
    c = clients[i[0]]
    label_client_name_val.config(text=c["name"])
    label_client_location_val.config(text=c["location"])
    label_client_theater_val.config(text=c.get("theater", ""))
    label_client_performances_val.config(text=", ".join(c.get("performances", [])))
    coords = get_coordinates(c["location"])
    if coords:
        map_clients.set_position(coords[0], coords[1])
        map_clients.set_zoom(12)

def add_client_gui():
    name         = entry_client_name.get()
    location     = entry_client_location.get()
    theater_name = entry_client_theater.get()
    performances = [p.strip() for p in entry_client_performances.get().split(",") if p.strip()]
    if not name or not location or not theater_name: return
    new = {"name": name, "location": location, "theater": theater_name,
           "performances": performances, "marker": None}
    clients.append(new)
    for t in theaters:
        if t["name"] == theater_name:
            t["clients"].append(new)
            break
    try:
        coords = get_coordinates(location)
        if coords:
            new["marker"] = set_marker(map_clients, coords, name, icon_client)
    except: pass
    entry_client_name.delete(0, END)
    entry_client_location.delete(0, END)
    entry_client_theater.delete(0, END)
    entry_client_performances.delete(0, END)
    refresh_clients()

def edit_client_gui():
    i = listbox_clients.curselection()
    if not i: return
    c = clients[i[0]]
    entry_client_name.delete(0, END)
    entry_client_location.delete(0, END)
    entry_client_theater.delete(0, END)
    entry_client_performances.delete(0, END)
    entry_client_name.insert(0, c["name"])
    entry_client_location.insert(0, c["location"])
    entry_client_theater.insert(0, c.get("theater", ""))
    entry_client_performances.insert(0, ", ".join(c.get("performances", [])))
    style_button(button_add_client, ACCENT2, TEXT)
    button_add_client.config(text="Zapisz zmiany", command=lambda idx=i[0]: save_client(idx))

def save_client(i):
    c = clients[i]
    if c["marker"]: c["marker"].delete()
    c["name"]         = entry_client_name.get()
    c["location"]     = entry_client_location.get()
    c["theater"]      = entry_client_theater.get()
    c["performances"] = [p.strip() for p in entry_client_performances.get().split(",") if p.strip()]
    try:
        coords = get_coordinates(c["location"])
        if coords:
            c["marker"] = set_marker(map_clients, coords, c["name"], icon_client)
    except: pass
    entry_client_name.delete(0, END)
    entry_client_location.delete(0, END)
    entry_client_theater.delete(0, END)
    entry_client_performances.delete(0, END)
    style_button(button_add_client)
    button_add_client.config(text="Dodaj klienta", command=lambda: add_client_gui())
    refresh_clients()

def delete_client_gui():
    i = listbox_clients.curselection()
    if not i: return
    c = clients[i[0]]
    if c["marker"]: c["marker"].delete()
    for t in theaters:
        if t["name"] == c.get("theater", ""):
            t["clients"] = [x for x in t["clients"] if x is not c]
            break
    clients.pop(i[0])
    refresh_clients()

def filter_clients():
    search = entry_client_filter.get().lower()
    listbox_clients.delete(0, END)
    for c in clients:
        if search in c["name"].lower() or search in c.get("theater", "").lower():
            listbox_clients.insert(END, c["name"])

def load_client_markers():
    for c in clients:
        try:
            coords = get_coordinates(c["location"])
            if coords:
                c["marker"] = set_marker(map_clients, coords, c["name"], icon_client)
            time.sleep(1.1)
        except: pass

refresh_clients()


# ========== PRACOWNICY ==========

frame_employee_list    = make_panel(tab_employees)
frame_employee_form    = make_panel(tab_employees)
frame_employee_details = make_panel(tab_employees)
frame_employee_map     = Frame(tab_employees, bg=BG)

frame_employee_list.grid(   row=0, column=0, padx=10, pady=10, sticky=N)
frame_employee_form.grid(   row=0, column=1, padx=10, pady=10, sticky=N)
frame_employee_details.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky=EW)
frame_employee_map.grid(    row=0, column=2, rowspan=2, padx=10, pady=10)

lbl = Label(frame_employee_list, text="Lista pracowników")
style_section_label(lbl); lbl.grid(row=0, column=0, columnspan=2, pady=(10,6), padx=10)

entry_employee_filter = Entry(frame_employee_list)
style_entry(entry_employee_filter)
entry_employee_filter.grid(row=1, column=0, padx=(10,4), pady=4)

btn_se = Button(frame_employee_list, text="Szukaj", command=lambda: filter_employees())
style_button(btn_se)
btn_se.grid(row=1, column=1, padx=(0,10), pady=4)

listbox_employees = Listbox(frame_employee_list, width=30, height=10)
style_listbox(listbox_employees)
listbox_employees.grid(row=2, column=0, columnspan=2, padx=10, pady=4)

btn_de = Button(frame_employee_list, text="Szczegóły", command=lambda: show_employee_details())
style_button(btn_de, ACCENT)
btn_de.grid(row=3, column=0, padx=(10,4), pady=4)

btn_ee = Button(frame_employee_list, text="Edytuj", command=lambda: edit_employee_gui())
style_button(btn_ee, SUBTEXT)
btn_ee.grid(row=3, column=1, padx=(0,10), pady=4)

btn_dele = Button(frame_employee_list, text="Usuń", command=lambda: delete_employee_gui())
style_button(btn_dele, DANGER)
btn_dele.grid(row=4, column=0, columnspan=2, padx=10, pady=(2,10))

lbl2 = Label(frame_employee_form, text="Nowy pracownik")
style_section_label(lbl2); lbl2.grid(row=0, column=0, columnspan=2, pady=(10,6), padx=10)

for row, text in [(1,"Imię i nazwisko:"), (2,"Lokalizacja:"), (3,"Teatr:")]:
    l = Label(frame_employee_form, text=text)
    style_label(l, sub=True)
    l.grid(row=row, column=0, sticky=W, padx=(10,4), pady=3)

entry_employee_name     = Entry(frame_employee_form)
entry_employee_location = Entry(frame_employee_form)
entry_employee_theater  = Entry(frame_employee_form)
for row, e in [(1, entry_employee_name), (2, entry_employee_location), (3, entry_employee_theater)]:
    style_entry(e)
    e.grid(row=row, column=1, padx=(0,10), pady=3)

button_add_employee = Button(frame_employee_form, text="Dodaj pracownika", command=lambda: add_employee_gui())
style_button(button_add_employee)
button_add_employee.grid(row=4, column=0, columnspan=2, pady=(6,12), padx=10)

frame_employee_details.config(bg=PANEL_BG)
lbl3 = Label(frame_employee_details, text="Szczegóły")
style_section_label(lbl3); lbl3.grid(row=0, column=0, columnspan=6, pady=(8,4), padx=10, sticky=W)

for col_idx, text in enumerate(["Nazwa:", "Lokalizacja:", "Teatr:"]):
    l = Label(frame_employee_details, text=text)
    style_label(l, sub=True)
    l.grid(row=1, column=col_idx*2, sticky=W, padx=(10,2))

label_employee_name_val     = Label(frame_employee_details, text="—"); style_label(label_employee_name_val, bold=True)
label_employee_location_val = Label(frame_employee_details, text="—"); style_label(label_employee_location_val, bold=True)
label_employee_theater_val  = Label(frame_employee_details, text="—"); style_label(label_employee_theater_val, bold=True)

for col_idx, lbl in enumerate([label_employee_name_val, label_employee_location_val, label_employee_theater_val]):
    lbl.grid(row=1, column=col_idx*2+1, sticky=W, padx=(0,16), pady=(0,8))

map_employees = tkintermapview.TkinterMapView(frame_employee_map, width=500, height=400)
map_employees.set_position(52.2, 21.0)
map_employees.set_zoom(6)
map_employees.grid(row=0, column=0)


def refresh_employees():
    listbox_employees.delete(0, END)
    for e in employees:
        listbox_employees.insert(END, e["name"])

def show_employee_details():
    i = listbox_employees.curselection()
    if not i: return
    e = employees[i[0]]
    label_employee_name_val.config(text=e["name"])
    label_employee_location_val.config(text=e["location"])
    label_employee_theater_val.config(text=e.get("theater", ""))
    coords = get_coordinates(e["location"])
    if coords:
        map_employees.set_position(coords[0], coords[1])
        map_employees.set_zoom(12)

def add_employee_gui():
    name         = entry_employee_name.get()
    location     = entry_employee_location.get()
    theater_name = entry_employee_theater.get()
    if not name or not location or not theater_name: return
    new = {"name": name, "location": location, "theater": theater_name, "marker": None}
    employees.append(new)
    for t in theaters:
        if t["name"] == theater_name:
            t["employees"].append(new)
            break
    try:
        coords = get_coordinates(location)
        if coords:
            new["marker"] = set_marker(map_employees, coords, name, icon_employee)
    except: pass
    entry_employee_name.delete(0, END)
    entry_employee_location.delete(0, END)
    entry_employee_theater.delete(0, END)
    refresh_employees()

def edit_employee_gui():
    i = listbox_employees.curselection()
    if not i: return
    e = employees[i[0]]
    entry_employee_name.delete(0, END)
    entry_employee_location.delete(0, END)
    entry_employee_theater.delete(0, END)
    entry_employee_name.insert(0, e["name"])
    entry_employee_location.insert(0, e["location"])
    entry_employee_theater.insert(0, e.get("theater", ""))
    style_button(button_add_employee, ACCENT2, TEXT)
    button_add_employee.config(text="Zapisz zmiany", command=lambda idx=i[0]: save_employee(idx))

def save_employee(i):
    e = employees[i]
    if e["marker"]: e["marker"].delete()
    e["name"]     = entry_employee_name.get()
    e["location"] = entry_employee_location.get()
    e["theater"]  = entry_employee_theater.get()
    try:
        coords = get_coordinates(e["location"])
        if coords:
            e["marker"] = set_marker(map_employees, coords, e["name"], icon_employee)
    except: pass
    entry_employee_name.delete(0, END)
    entry_employee_location.delete(0, END)
    entry_employee_theater.delete(0, END)
    style_button(button_add_employee)
    button_add_employee.config(text="Dodaj pracownika", command=lambda: add_employee_gui())
    refresh_employees()

def delete_employee_gui():
    i = listbox_employees.curselection()
    if not i: return
    e = employees[i[0]]
    if e["marker"]: e["marker"].delete()
    for t in theaters:
        if t["name"] == e.get("theater", ""):
            t["employees"] = [x for x in t["employees"] if x is not e]
            break
    employees.pop(i[0])
    refresh_employees()

def filter_employees():
    search = entry_employee_filter.get().lower()
    listbox_employees.delete(0, END)
    for e in employees:
        if search in e["name"].lower() or search in e.get("theater", "").lower():
            listbox_employees.insert(END, e["name"])

def load_employee_markers():
    for e in employees:
        try:
            coords = get_coordinates(e["location"])
            if coords:
                e["marker"] = set_marker(map_employees, coords, e["name"], icon_employee)
            time.sleep(1.1)
        except: pass

refresh_employees()


# ========== WYSZUKIWARKA ==========

frame_views_filters = make_panel(tab_views)
frame_views_results = make_panel(tab_views)
frame_views_map     = Frame(tab_views, bg=BG)

frame_views_filters.grid(row=0, column=0, padx=10, pady=10, sticky=N)
frame_views_results.grid(row=0, column=1, padx=10, pady=10, sticky=N)
frame_views_map.grid(    row=0, column=2, padx=10, pady=10, sticky=N)

lbl = Label(frame_views_filters, text="Filtry")
style_section_label(lbl); lbl.grid(row=0, column=0, columnspan=2, pady=(10,6), padx=10)

l1 = Label(frame_views_filters, text="Nazwa teatru:")
style_label(l1, sub=True)
l1.grid(row=1, column=0, sticky=W, padx=(10,4), pady=3)

entry_filter_theater = Entry(frame_views_filters)
style_entry(entry_filter_theater)
entry_filter_theater.grid(row=1, column=1, padx=(0,10), pady=3)

btn_ct = Button(frame_views_filters, text="Klienci tego teatru", command=lambda: show_clients_by_theater())
style_button(btn_ct)
btn_ct.grid(row=2, column=0, columnspan=2, padx=10, pady=3, sticky=EW)

btn_et = Button(frame_views_filters, text="Pracownicy tego teatru", command=lambda: show_employees_by_theater())
style_button(btn_et, SUBTEXT)
btn_et.grid(row=3, column=0, columnspan=2, padx=10, pady=3, sticky=EW)

l2 = Label(frame_views_filters, text="Imię i nazwisko klienta:")
style_label(l2, sub=True)
l2.grid(row=4, column=0, sticky=W, padx=(10,4), pady=(15,3))

entry_filter_client = Entry(frame_views_filters)
style_entry(entry_filter_client)
entry_filter_client.grid(row=4, column=1, padx=(0,10), pady=(15,3))

btn_pc = Button(frame_views_filters, text="Spektakle klienta", command=lambda: show_performances_by_client())
style_button(btn_pc, ACCENT2, TEXT)
btn_pc.grid(row=5, column=0, columnspan=2, padx=10, pady=(3,12), sticky=EW)

lbl2 = Label(frame_views_results, text="Wyniki")
style_section_label(lbl2); lbl2.grid(row=0, column=0, pady=(10,6), padx=10)

listbox_views = Listbox(frame_views_results, width=50, height=20)
style_listbox(listbox_views)
listbox_views.grid(row=1, column=0, padx=10, pady=(0,10))

map_views = tkintermapview.TkinterMapView(frame_views_map, width=500, height=400)
map_views.set_position(52.2, 21.0)
map_views.set_zoom(6)
map_views.grid(row=0, column=0)


def show_clients_by_theater():
    theater_name = entry_filter_theater.get()
    listbox_views.delete(0, END)
    map_views.delete_all_marker()
    result = [c for c in clients if theater_name.lower() in c.get("theater", "").lower()]
    if not result:
        listbox_views.insert(END, "Brak klientów dla tego teatru")
        return
    for c in result:
        listbox_views.insert(END, f"{c['name']} – {c['location']}")
        try:
            coords = get_coordinates(c["location"])
            if coords:
                map_views.set_marker(coords[0], coords[1], text=c["name"],
                                     icon=icon_client, icon_anchor="center",
                                     font=(FONT, 10, "bold"), text_color=TEXT)
        except: pass

def show_employees_by_theater():
    theater_name = entry_filter_theater.get()
    listbox_views.delete(0, END)
    map_views.delete_all_marker()
    result = [e for e in employees if theater_name.lower() in e.get("theater", "").lower()]
    if not result:
        listbox_views.insert(END, "Brak pracowników dla tego teatru")
        return
    for e in result:
        listbox_views.insert(END, f"{e['name']} – {e['location']}")
        try:
            coords = get_coordinates(e["location"])
            if coords:
                map_views.set_marker(coords[0], coords[1], text=e["name"],
                                     icon=icon_employee, icon_anchor="center",
                                     font=(FONT, 10, "bold"), text_color=TEXT)
        except: pass

def show_performances_by_client():
    client_name = entry_filter_client.get()
    listbox_views.delete(0, END)
    map_views.delete_all_marker()
    found = None
    for c in clients:
        if c["name"].lower() == client_name.lower():
            found = c
            break
    if not found:
        listbox_views.insert(END, "Nie znaleziono klienta")
        return
    try:
        coords = get_coordinates(found["location"])
        if coords:
            map_views.set_marker(coords[0], coords[1], text=found["name"],
                                 icon=icon_client, icon_anchor="center",
                                 font=(FONT, 10, "bold"), text_color=TEXT)
    except: pass
    performances = found.get("performances", [])
    if not performances:
        listbox_views.insert(END, "Brak spektakli dla tego klienta")
        return
    for p in performances:
        listbox_views.insert(END, p)


def on_start():
    init_icons()
    import threading
    threading.Thread(target=_load_all_markers, daemon=True).start()

def _load_all_markers():
    load_theater_markers()
    load_client_markers()
    load_employee_markers()

root.after(100, on_start)
root.mainloop()
