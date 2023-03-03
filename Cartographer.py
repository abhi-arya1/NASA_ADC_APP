# This program is used to create the heightmap and slope map from the data

import csv
import FolderCreator as fc
from ast import literal_eval
from PIL import Image
import Constants as c

astar_data_path = fc.data_path + "/AStarRawData.csv"
with open(astar_data_path, mode="r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    full_list = list(csv_reader)
    csv_file.close()

misc_path = fc.data_path + "/MiscData.csv"
with open(misc_path, mode="r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    max_z = float(list(csv_reader)[0][0])
    #print(max_z)
    csv_file.close()


def calculate_color(height):
    color = 255 - (height * 255 / max_z)
    return int(color), int(color), int(color)


def calc_rgb_color(height):
    r, g, b = 0, 0, 0
    if height / max_z <= 1/3:
        b = height * 255 / max_z
    elif height / max_z <= 2/3:
        g = height * 255 / max_z
    else:
        r = height * 255 / max_z
    return (int(r), int(g), int(b))


def draw_points():
    for i in range(len(full_list)):
        for j in range(len(full_list[i])):
            color = calculate_color(float(literal_eval(full_list[j][i])[2]))
            x_pos = j
            y_pos = i
            # print(x_pos, y_pos)
            canvas.putpixel((int(x_pos), int(y_pos)), color)
            # note that there is a bit of data loss here.
            # Ideally, we'd make the final image have a size equal to the maximum span of the x and y data

def draw_colors():
    for i in range(len(full_list)):
        for j in range(len(full_list[i])):
            color = calc_rgb_color(float(literal_eval(full_list[j][i])[2]))
            x_pos = j
            y_pos = i
            # print(x_pos, y_pos)
            canvas.putpixel((int(x_pos), int(y_pos)), color)

def draw_slopes():
    for i in range(len(full_list)):
        for j in range(len(full_list[i])):
            color = (255, 0, 0)
            if float(literal_eval(full_list[j][i])[3]) < 20:
                color = (255, 255, 0)
            if float(literal_eval(full_list[j][i])[3]) < 8:
                color = (0, 255, 0)
            x_pos = j
            y_pos = i
            #print(x_pos, y_pos)
            canvas.putpixel((int(x_pos), int(y_pos)), color)

def draw_path(path, image, color):
    for i in range(len(path)):
        image.putpixel(path[0], path[1], color)
    return image


if __name__ == "__main__":
    canvas = Image.new('RGBA', (c.SIZE_CONSTANT, c.SIZE_CONSTANT), 'blue')
    draw_points()
    canvas.save(fc.images_path + '/RAW_heightmap.png') # must save here for a proper read from Ursina
    print("Created ursina_heightmap.png")
    draw_slopes()
    canvas.save(fc.parent_path + '/slopemap.png')
    print("Created slopemap.png")
    draw_colors()
    canvas.save(fc.parent_path + '/heightkey.png')
    print("Created heightkey.png")

    upscaled = Image.open(fc.images_path + '/RAW_heightmap.png')
    downscaled = upscaled.resize((81, 81))
    downscaled.save(fc.parent_path + '/processed_heightmap.png')




