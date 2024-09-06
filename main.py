import numpy as np
import matplotlib.pyplot as plt


Apd = 10 ** (-4)
gf = 1
n = 1.5
psi_max = (90 * np.pi) / 180
gc = (n ** 2) / np.sin(psi_max) ** 2
fi12 = (60 * np.pi) / 180
m = (-np.log(2)) / np.log(np.cos(fi12))
Popt = 3
wall_length = 8
wall_width = 4
h = 4
step = 0.01


lamps = np.array([[2, 1, h],
                  [2, 3, h],
                  [6, 1, h],
                  [6, 3, h]])


def prec_to_binary(prec_value, max_prec, num_bits=8):
    normalized_prec = prec_value / max_prec
    binary_prec = bin(int(normalized_prec * (2 ** num_bits - 1)))[2:]
    binary_prec = binary_prec.zfill(num_bits)
    return binary_prec


def find_square_coordinates():
    num_xmas = int(wall_length / step) + 1
    num_ymas = int(wall_width / step) + 1
    num_lamps = len(lamps)
    floor_matrix = np.zeros((num_ymas, num_xmas, num_lamps))


    xmas = np.arange(0, wall_length + step, step)
    ymas = np.arange(0, wall_width + step, step)


    prec_values = [input(f"Введіть значення Prec для лампи {i + 1} (у вигляді 8 біт): ") for i in range(4)]


    for lamp_idx in range(num_lamps):
        for i in range(num_ymas):
            for j in range(num_xmas):
                x_quad = xmas[j]
                y_quad = ymas[i]
                z_quad = 0


                x_lamp = lamps[lamp_idx, 0]
                y_lamp = lamps[lamp_idx, 1]
                z_lamp = lamps[lamp_idx, 2]


                d = np.sqrt((z_lamp - z_quad) ** 2 + (x_lamp - x_quad) ** 2 + (y_lamp - y_quad) ** 2)


                Hlos = ((m + 1) * Apd * (h / d) ** m * gf * gc * (h / d)) / (2 * np.pi * (d ** 2 + h ** 2))


                Prec = Hlos * Popt


                floor_matrix[i, j, lamp_idx] = Prec


    max_prec = np.max(floor_matrix)
    found = False
    found_x = None
    found_y = None


 
    for exclude_idx in range(4):
        comparison_values = ["" if i == exclude_idx else prec_values[i] for i in range(4)]


        for i in range(num_ymas):
            for j in range(num_xmas):
                binary_prec_values = [
                    prec_to_binary(floor_matrix[i, j, lamp_idx], max_prec) for lamp_idx in range(num_lamps)
                ]


                binary_prec_values[exclude_idx] = ""


                if all(binary_prec_values[i] == comparison_values[i] for i in range(4)):
                    found = True
                    found_x = xmas[j]
                    found_y = ymas[i]


                    print(f"Знайдено квадрат з координатами X: {found_x}, Y: {found_y}")
                    break


            if found:
                break


        if found:
            break


    if not found:
        print("Спотворено 2 або більше сигналів.")


    fig, axes = plt.subplots(2, 2, figsize=(10, 10))


    for lamp_idx in range(num_lamps):
        ax = axes[lamp_idx // 2, lamp_idx % 2]
        im = ax.imshow(floor_matrix[:, :, lamp_idx], extent=[0, wall_length, wall_width, 0], cmap='jet')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title(f'Лампа {lamp_idx + 1}')
        fig.colorbar(im, ax=ax)


    plt.tight_layout()
    plt.show()


print("Починаємо пошук:")
find_square_coordinates()
