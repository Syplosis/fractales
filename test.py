from PIL import Image, ImageDraw, ImageTk
from tkinter import Tk, Label, Button, Entry
import cmath

# Configuration Tkinter
root = Tk()
root.title("Fractale de Mandelbrot")

# Paramètres de l'image
window_size = (300, 300)
division_window = window_size[0] // 2.5
shifting_coef = 10

# Coefficients de couleur (modifiable dynamiquement)
a, b, d = 17, 2, 4

gap = 0
out = Image.new("RGBA", window_size, (0, 0, 0, 0))
drawable_image = 0

def generation(gap_offset, division_window, x_start=0, x_end=0, y_start=0, y_end=0, pil_image=out):
    """
    Génère la fractale de Mandelbrot sur l'image.
    """
    global drawable_image
    if x_start == 0:
        x_start = -pil_image.width // 2 + gap_offset
    if x_end == 0:
        x_end = pil_image.width // 2 + 1 - gap_offset
    if y_start == 0:
        y_start = -pil_image.height // 2
    if y_end == 0:
        y_end = pil_image.height // 2 + 1
    
    drawable_image = ImageDraw.Draw(pil_image)
    for x in range(x_start, x_end):
        for y in range(y_start, y_end):
            c = complex(x / division_window, y / division_window)
            z = 0
            for i in range(50):
                ######################################################
                ######################################################
                z = z * z + c
                ######################################################
                ######################################################
                if abs(z) > 2:
                    drawable_image.point((x - gap_offset + pil_image.width // 2, y + pil_image.height // 2), 
                                         fill=((a * i) % 255, (b * i) % 255, (d * i) % 255, 255))
                    break
            else:
                drawable_image.point((x - gap_offset + pil_image.width // 2, y + pil_image.height // 2), fill=(0, 0, 0, 255))

def fast_image_shift(x_offset, y_offset, image):
    """
    Décale rapidement l'image en appliquant un décalage horizontal et vertical.
    Remplit les zones hors limites avec du blanc.
    """
    width, height = image.size

    # Créer une nouvelle image avec un fond blanc
    shifted_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))

    # Calcul des zones de découpe et de collage
    x_start_src = max(0, -x_offset)
    y_start_src = max(0, -y_offset)
    x_end_src = width - max(0, x_offset)
    y_end_src = height - max(0, y_offset)

    x_start_dest = max(0, x_offset)
    y_start_dest = max(0, y_offset)

    # Découper la région source
    cropped_region = image.crop((x_start_src, y_start_src, x_end_src, y_end_src))

    # Coller la région découpée dans l'image décalée
    shifted_image.paste(cropped_region, (x_start_dest, y_start_dest))

    return shifted_image

def update_image():
    """
    Met à jour l'image affichée dans Tkinter.
    """
    global tkinter_image, out
    tkinter_image = ImageTk.PhotoImage(out)
    label = Label(root, image=tkinter_image)
    label.grid(row=1, column=1, columnspan=3)

def move_to_the_left():
    global gap, out
    # Décale l'image vers la gauche
    out = fast_image_shift(-shifting_coef, 0, out)
    gap += shifting_coef  # Ajuste le décalage total
    
    # Génère les nouvelles parties manquantes à gauche
    generation(
        gap, 
        division_window, 
        x_start=window_size[0] // 2 - gap,  # Début de la nouvelle portion à gauche
        x_end=window_size[0] // 2 + gap,  # Fin de la nouvelle portion à gauche
        pil_image=out
    )
    update_image()


def move_to_the_right():
    global gap, out
    out = fast_image_shift(shifting_coef, 0, out)
    gap -= shifting_coef  # Décaler l'image en modifiant 'gap'
    generation(gap, division_window, x_end=-window_size[0] // 2 + shifting_coef, pil_image=out)
    update_image()

def zoom_in():
    global division_window
    division_window *= 1.1
    generation(gap, division_window)
    update_image()

def zoom_out():
    global division_window
    division_window /= 1.1
    generation(gap, division_window)
    update_image()

def reset():
    """
    Réinitialise les paramètres de la fractale.
    """
    global gap, division_window, out
    gap = 0
    division_window = window_size[0] // 2.5
    out = Image.new("RGBA", window_size, (255, 255, 255, 255))
    generation(gap, division_window)
    update_image()

def update_colors():
    global a, b, d
    try:
        a = int(entry_a.get())
        b = int(entry_b.get())
        d = int(entry_d.get())
        generation(gap, division_window)
        update_image()
    except ValueError:
        print("Entrées invalides pour les coefficients.")

# Générer l'image initiale
generation(gap, division_window)

# Afficher l'image dans Tkinter
tkinter_image = ImageTk.PhotoImage(out)
label = Label(root, image=tkinter_image)
label.grid(row=1, column=1, columnspan=3)

# Boutons de navigation
left_button = Button(root, text="<-", command=move_to_the_left)
left_button.grid(row=2, column=0)
right_button = Button(root, text="->", command=move_to_the_right)
right_button.grid(row=2, column=4)
zoom_in_button = Button(root, text="Zoom +", command=zoom_in)
zoom_in_button.grid(row=2, column=2)
zoom_out_button = Button(root, text="Zoom -", command=zoom_out)
zoom_out_button.grid(row=2, column=3)
reset_button = Button(root, text="Reset", command=reset)
reset_button.grid(row=2, column=1)

# Entrées pour les coefficients de couleur
entry_a = Entry(root, width=5)
entry_a.insert(0, str(a))
entry_a.grid(row=3, column=1)
entry_b = Entry(root, width=5)
entry_b.insert(0, str(b))
entry_b.grid(row=3, column=2)
entry_d = Entry(root, width=5)
entry_d.insert(0, str(d))
entry_d.grid(row=3, column=3)

update_color_button = Button(root, text="Update Colors", command=update_colors)
update_color_button.grid(row=4, column=2)

# Lancer l'application Tkinter
root.mainloop()
