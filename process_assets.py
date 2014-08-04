#!/bin/env python

import os
import sys
import tempfile
from xml.etree.ElementTree import ElementTree
import subprocess
from PIL import Image
import platform

if platform.system() == "Darwin":
    inkscape_path = "/Applications/Inkscape.app/Contents/Resources/bin/inkscape"
elif platform.system() == "Windows":
    inkscape_path = os.environ["ProgramFiles"] + "\\Inkscape\\inkscape.exe"
else:
    inkscape_path = "inkscape"

default_target_dpi = [
    ('xxxhdpi', 640),
    ('xxhdpi', 480),
    ('xhdpi', 320),
    ('hdpi', 240),
    ('mdpi', 160),
    ('ldpi', 120)
]


def to_black_or_transparent(color):
    if color[3] == 0:
        return 0, 0, 0, 0
    else:
        return 0, 0, 0, 255


def extract_9patch(file_, out_file_):
    document = ElementTree()
    document.parse(file_)

    root = document.getroot()
    for elem in root.iter("{http://www.w3.org/2000/svg}g"):
        layer_name = elem.get("{http://www.inkscape.org/namespaces/inkscape}label")
        layer_id = elem.get("id")
        if layer_name == "9patch" or layer_id == "_x39_patch":
            elem.set('style', '')
            elem.set('display', '')
        else:
            elem.set('style', 'display:none')
            elem.set('display', 'none')

    document.write(out_file_)


def create_9_patch_for_dpi(file_, dpi_, out_file_):
    tmp_path = tempfile.gettempdir()
    tmp_9patch_svg = tmp_path + os.path.sep + '9patch.svg'
    tmp_9patch_png = tmp_path + os.path.sep + '9patch.png'

    extract_9patch(file_, tmp_9patch_svg)

    subprocess.check_output([inkscape_path, "-d", str(dpi_), "-e", tmp_9patch_png, tmp_9patch_svg])

    im = Image.open(tmp_9patch_png)
    pix = im.load()
    new_size = (im.size[0] + 2, im.size[1] + 2)
    new_image = Image.new("RGBA", new_size, (255, 255, 255, 0))
    new_pix = new_image.load()

    for x in range(0, im.size[0]):
        data = to_black_or_transparent(pix[x, 0])
        new_pix[x + 1, 0] = data
        data = to_black_or_transparent(pix[x, im.size[1] - 1])
        new_pix[x + 1, new_size[1] - 1] = data

    for y in range(0, im.size[1]):
        data = to_black_or_transparent(pix[0, y])
        new_pix[0, y + 1] = data
        data = to_black_or_transparent(pix[im.size[0] - 1, y])
        new_pix[new_size[0] - 1, y + 1] = data

    subprocess.check_output([inkscape_path, "-d", str(dpi_), "-e", out_file_, file_])

    im = Image.open(out_file_)
    new_image.paste(im, (1, 1))

    new_image.save(out_file_)


def process_file(file_, dpi_fix_, is_9patch_, resources_dir_):
    print "Processing " + file_ + ":",
    for (alias_, dpi_) in target_dpi:
        out_dir = resources_dir_ + os.path.sep + 'drawable-' + alias_ + os.path.sep
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        out_file = out_dir + os.path.basename(file_.replace('.svg', '.png'))
        print str(dpi_) + "...",
        inkscape_dpi = round(dpi_ * dpi_fix_)
        if is_9patch_:
            create_9_patch_for_dpi(file_, inkscape_dpi, out_file)
        else:
            subprocess.check_output([inkscape_path, "-d", str(inkscape_dpi), "-e", out_file, file_])
    print "Done"


assets_dir = 'assets'
resources_dir = 'res'
document_dpi = 160

target_dpi = default_target_dpi
inkscape_dpi_fix = 90.0 / document_dpi

assets = []
for assets_dir, _, files in os.walk(assets_dir):
    for file_name in files:
        if file_name.endswith('.svg'):
            assets.append(os.path.join(assets_dir, file_name))

for svg_file in assets:
    if svg_file.endswith('.9.svg'):
        process_file(svg_file, inkscape_dpi_fix, True, resources_dir)
    else:
        process_file(svg_file, inkscape_dpi_fix, False, resources_dir)
