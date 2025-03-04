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
default_division = window_size[0] // 4.6  # POur un zoom de départ plus ou moins grand, changer la constante
shift_step = 10 # Pour decaler plus ou moins rapidement l'image

# Variables globales
gap = 0
division = default_division
color_a, color_b, color_d = 17, 2, 4
canvas_image = Image.new("RGBA", window_size, (0, 0, 0, 0))

# Tkinter setup
root = Tk()
root.title("Fractal Viewer")


def generate_image(gap_offset=0, division=120, x_start=None, x_end=None, y_start=None, y_end=None, pil_image=canvas_image, a=color_a, b=color_b, d=color_d):
    """
    Generates a Mandelbrot fractal on the given image.
    """
    width, height = pil_image.size

    x_start = x_start if x_start is not None else -width // 2 + gap_offset
    x_end = x_end if x_end is not None else width // 2 + 1 - gap_offset
    y_start = y_start if y_start is not None else -height // 2
    y_end = y_end if y_end is not None else height // 2 + 1
    print(x_start, x_end, y_start, y_end)
    draw = ImageDraw.Draw(pil_image)

    for x in range(x_start, x_end):
        for y in range(y_start, y_end):
            c = complex(x / division, y / division)
            z = 0

            for i in range(50):
                ######################################################
                # Ici tu peux changer la fonction
                # tu as z le nombre sur lequel tu execute ta fonction a chaque réccurence
                # et c c'est le nombre qui dépends de la place du pixel dans le plan complexe
                # ici, c = x + iy
                z = z *z + c
                # Exemple avec le module cmath : z = z * cmath.exp(z) + c (avec ici exp pour exponentielle)
                ######################################################
                if abs(z) > 2:
                    draw.point((x - gap_offset + width // 2, y + height // 2),
                               fill=((a * i) % 255, (b * i) % 255, (d * i) % 255, 255))
                    break
            else:
                draw.point((x - gap_offset + width // 2, y + height // 2), fill=(0, 0, 0, 255))


# FOnction pour gerer rapidement la translation horizontale d'une image (plus rapide que de generer tout l'image a chaque decalage)
# On décale donc l'image, puis avec une autre fonction on genere seulement la partie manquante
def shift_image(x_offset, y_offset, image):
    """
    Shifts the image horizontally and vertically, filling empty areas with transparency.
    """
    width, height = image.size

    shifted_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))

    x_start_src = max(0, -x_offset)
    y_start_src = max(0, -y_offset)
    x_end_src = width - max(0, x_offset)
    y_end_src = height - max(0, y_offset)

    x_start_dest = max(0, x_offset)
    y_start_dest = max(0, y_offset)

    cropped_region = image.crop((x_start_src, y_start_src, x_end_src, y_end_src))
    shifted_image.paste(cropped_region, (x_start_dest, y_start_dest))

    return shifted_image

# Fonction simple pour mettre a jour l'image generée dans les fonctions suivantes (précédement executées)
def update_image():
    global tkinter_image, canvas_image
    tkinter_image = ImageTk.PhotoImage(canvas_image)
    label.config(image=tkinter_image)

# Fonction qui gere le decalage vers la gauche 
def move_left():
    global gap, canvas_image
    canvas_image = shift_image(-shift_step, 0, canvas_image)
    gap += shift_step
    generate_image(gap_offset=gap, division=division, x_start=window_size[0] // 2 -gap, x_end=window_size[0] // 2 + gap, pil_image=canvas_image, a=color_a, b=color_b, d=color_d)
    update_image()

# Fonction qui gere le decalage vers la gauche 
def move_right():
    global gap, canvas_image
    canvas_image = shift_image(shift_step, 0, canvas_image)
    gap -= shift_step
    generate_image(gap_offset=gap, division=division, x_end=-window_size[0] // 2 + shift_step, pil_image=canvas_image, a=color_a, b=color_b, d=color_d)
    update_image()

# Fonction qui gere le zoom
def zoom_in():
    global division
    division *= 1.1
    generate_image(gap_offset=gap, division=division, pil_image=canvas_image, a=color_a, b=color_b, d=color_d)
    update_image()

# Fonction qui gere le dezoom
def zoom_out():
    global division
    division /= 1.1
    generate_image(gap_offset=gap, division=division, pil_image=canvas_image, a=color_a, b=color_b, d=color_d)
    update_image()

# FOnction qui remet la fractale comme elle était au début
def reset_image():
    global gap, division, canvas_image
    gap = 0
    division = default_division
    canvas_image = Image.new("RGBA", window_size, (0, 0, 0, 0))
    generate_image(gap_offset=gap, division=division, pil_image=canvas_image, a=color_a, b=color_b, d=color_d)
    update_image()

# Fonction qui gère le changement de couleur
def update_colors():
    try:
        color_a = int(entry_a.get())
        color_b = int(entry_b.get())
        color_d = int(entry_d.get())
        generate_image(gap, division, a=color_a, b=color_b, d=color_d)
        update_image()
    except ValueError:
        print("Invalid input for color coefficients.")

# FOnction pour l'enregistrement de l'image
def save_image():
    """
    Opens a file dialog to save the current image to a specified location.
    """
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if file_path:
        canvas_image.save(file_path)
        print(f"Image saved to {file_path}")

# Generer l'image de départ
generate_image(gap_offset=gap, division=division, pil_image=canvas_image, a=color_a, b=color_b, d=color_d)
tkinter_image = ImageTk.PhotoImage(canvas_image)
label = Label(root, image=tkinter_image)
label.grid(row=0, column=0, columnspan=5)

# Boutton du module tkinter
Button(root, text="<", command=move_left).grid(row=1, column=0)
Button(root, text=">", command=move_right).grid(row=1, column=1)
Button(root, text="Zoom +", command=zoom_in).grid(row=1, column=2)
Button(root, text="Zoom -", command=zoom_out).grid(row=1, column=3)
Button(root, text="Reset", command=reset_image).grid(row=1, column=4)
Button(root, text="Save", command=save_image).grid(row=2, column=0)

# Entrée de texte de tkinter et ici, gestion des couleurs
entry_a = Entry(root, width=5)
entry_a.insert(0, str(color_a))
entry_a.grid(row=2, column=1)
entry_b = Entry(root, width=5)
entry_b.insert(0, str(color_b))
entry_b.grid(row=2, column=2)
entry_d = Entry(root, width=5)
entry_d.insert(0, str(color_d))
entry_d.grid(row=2, column=3)
Button(root, text="Update Colors", command=update_colors).grid(row=2, column=4)

root.mainloop()