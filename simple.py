# Quand tu utilise le programme, il est pas super bien optimisé, donc notament quand tu decale
# l'image, il faut pas aller trop vite sinon tu vas te retrouver avec des grandes bandes blanches
# mais sinon tout est censé marcher !
# PS : Le boutton pour changer les couleurs marche pas très bien, je t'enverras une deuxieme version
# En attandant, tu peux toujours les modifier a la ligne 32

# Ca c'est les deux modules que tu dois avoir obligatoirement
# Si tu les a pas, normalement c'est assez simple
# Voila un lien qui t'explique comment ca marche https://www.guru99.com/fr/how-to-install-pip-on-windows.html?gpp&gpp_sid
# Quand tu auras compris comment ca marche
# Tape ca dans un terminal cmd
# pip install PIL
# pip install tkinter
# Si tu n'y arrives pas, peut etre que ta version de pip est trop ancienne, demande moi
from PIL import Image, ImageDraw, ImageTk
from tkinter import Tk, Label, Button, Entry, filedialog

# Ca c'est un module qui n'est pas nécessaire pour ce programme mais que tu peux
# utiliser si jamais tu veux utiliser des fonctions mathématiques plus compliquées ( qui
# demanderont surement plus de temps a calculer) comme des exponentielles ...
# Voila la documentations https://docs.python.org/fr/3/library/cmath.html
import cmath

# Constantes
window_size = (1000, 300)  # Taille de la fractales
default_division = window_size[0] // 2.5  # POur un zoom de départ plus ou moins grand, changer la constante
shift_step = 10 # Pour decaler plus ou moins rapidement l'image

# Variables globales
division = default_division
color_a, color_b, color_c = 17, 2, 4   # COULEUR A CHANGER EN FORMAT R, G, B
canvas_image = Image.new("RGBA", window_size, (0, 0, 0, 0))

# Tkinter setup
root = Tk()
root.title("Fractal Viewer")


def generate_image(division=120, x_start=-canvas_image.size[0]//2, x_end=canvas_image.size[0]//2, y_start=-canvas_image.size[1]//2, y_end=canvas_image.size[1]//2):

    global canvas_image  #POur pouvoir utiliser cette variable partout
    canvas_image = Image.new("RGBA", (x_end-x_start, y_end-y_start), (0, 0, 0, 0)) # On genere une image blanche de la taille demandée
    draw = ImageDraw.Draw(canvas_image) # En rapport avec le module PIL

    for x in range(x_start, x_end): # On boucle sur la partie Reelle
        for y in range(y_start, y_end): # Pour chaque réel, on boucle sur la partie imaginaire
            c = complex(x / division, y / division) # On genre un nombre complexe sous forme algebrique
            z = c

            for i in range(50): # On réalise un grand nombre de fois (ici arbitrairement 50)
                ######################################################
                # Ici tu peux changer la fonction
                # tu as z le nombre sur lequel tu execute ta fonction a chaque réccurence
                # et c c'est le nombre qui dépends de la place du pixel dans le plan complexe
                # ici, c = x + iy
                try:
                    z = z - (z*z*z-1)/(3*z*z)
                except:
                    print("Valeur interdite (0)")
                # Exemple avec le module cmath : z = z * cmath.exp(z) + c (avec ici exp pour exponentielle)
                ######################################################
                if abs(z) > 2:
                    draw.point((x+canvas_image.size[0]//2, y +canvas_image.size[1]// 2),
                               fill=((color_a * i) % 255, (color_b * i) % 255, (color_c * i) % 255, 255))
                    break
            else:
                draw.point((x + canvas_image.size[0]// 2, y + canvas_image.size[1]// 2), fill=(0, 0, 0, 255))

# Fonction simple pour mettre a jour l'image generée dans les fonctions suivantes (précédement executées)
def update_image():
    global tkinter_image, canvas_image  # Si tu te poses encore des questions sur la méthode global, cf "portée d'une variable"
    tkinter_image = ImageTk.PhotoImage(canvas_image)
    label.config(image=tkinter_image)

# FOnction pour l'enregistrement de l'image
def save_image():
    """
    Fonction qui sauvegarde la fractales generée. Fonction compliquée, mais inutile a comprendre
    """
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if file_path:
        canvas_image.save(file_path)
        print(f"Image saved to {file_path}")

# Fonction qui regenere l'image dans les dimensions demandées
def reset():
    x_start = int(entry_x_start.get()) # On prends les valeurs dans les entrée de texte de l'interface graphique
    x_end = int(entry_x_end.get())
    y_start = int(entry_y_start.get())
    y_end = int(entry_y_end.get())
    generate_image(division, x_start, x_end, y_start, y_end)
    update_image()

# Generer l'image de départ
generate_image(division=division)
tkinter_image = ImageTk.PhotoImage(canvas_image)
label = Label(root, image=tkinter_image)
label.grid(row=0, column=0, columnspan=5)  # La fonction grid est utilisée pour "imprimer" l'element sur l'interface graphique

# Gestion des boutons et des Entry(Entrée de texte) avec le module tkinter
Button(root, text="Save", command=save_image).grid(row=2, column=0)
Button(root, text="Update", command=reset).grid(row=2, column=1)

entry_x_start = Entry(root)
entry_x_start.insert(0, str(-window_size[0]//2))
entry_x_start.grid(row=1, column=0)

entry_x_end = Entry(root)
entry_x_end.insert(0, str(window_size[0]//2))
entry_x_end.grid(row=1, column=1)

entry_y_start = Entry(root)
entry_y_start.insert(0, str(-window_size[1]//2))
entry_y_start.grid(row=1, column=2)

entry_y_end = Entry(root)
entry_y_end.insert(0, str(window_size[1]//2))
entry_y_end.grid(row=1, column=3)

root.mainloop()