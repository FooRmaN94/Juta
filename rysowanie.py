from PIL import Image, ImageDraw, ImageFont


def make_flyer(data):
    # set dimensions of single page DPI 300 for A4
    width = 2480
    height = 3508
    # load static pictures with Pillow
    head_image = Image.open("header.png")
    foot_image = Image.open("footer.png")
    hit = Image.open("hit.png")
    # define margins and grid dimensions (3x4 elements or 3x3 if first page)
    element_vertical_margin = 30
    element_horizontal_margin = 10
    site_margin = 50
    footer_h = foot_image.height
    element_h = (height - 2 * site_margin - footer_h) / 4 - element_vertical_margin
    element_w = (width - 2 * site_margin) / 3 - element_horizontal_margin
    # define pages container (
    pages = []
    page = 1

    # loop through all elements
    while len(data):
        # set current pointers (for column and rows) to 0 (first element on page)
        curr_row = 0
        curr_col = 0
        # Create fresh page (blank white paper) and set it to PNG
        img = Image.new('RGB', (width, height), color='white')
        img.putalpha(255)
        # if current page is first, add header and skip one row
        if page == 1:
            # Header
            img.paste(head_image, (site_margin, site_margin))
            curr_row = 1

        # Footer
        # load footer and paste it to the bottom
        new_max = height - site_margin - footer_h
        img.paste(foot_image, (site_margin, new_max))

        # sweep trought all positions and paste new elementes
        while curr_row < 4:
            while curr_col < 3:
                # check if there is any data left
                if len(data) > 0:
                    # remove first item on the list and assign it to the element variable if there's none element left, break the loop
                    element = data.pop(0)
                else:
                    break
                # calculate new point (top-left) where new image should be pasted
                h_start = site_margin + curr_col * (element_horizontal_margin + element_w)
                v_start = site_margin + curr_row * (element_vertical_margin + element_h)

                # make an image for element
                element_image = paste_image(element)
                if element["atrybut"].find("hit") > -1:
                    element_image.paste(hit, (element_image.width - hit.width, 0), hit)
                # add text to element
                element_image = add_text(element, element_image)
                img.paste(element_image, (int(h_start), int(v_start)), mask=element_image)
                # increase pointers value. If element had attribute "podwojny" skip additional column
                if element["atrybut"].find("podwojna") > -1:
                    curr_col += 1
                curr_col += 1
            curr_col = 0
            curr_row += 1
        # add freshly created page to page list and increase page counter
        pages.append((img.copy().convert('RGB')))
        page += 1

    # save to pdf
    pages[0].save("ulotka.pdf","PDF",resolution=300.0, save_all=True,append_images=pages[1:])


def add_text(data, img):
    # create fonts
    name_font = ImageFont.truetype("arialbd.ttf", 36)
    netto_font = ImageFont.truetype("arialbd.ttf", 80)
    brutto_font = ImageFont.truetype("arialbd.ttf", 36)
    # calculate the offset for prices (to justify to the right)
    offset_netto = netto_font.getlength(data["cena netto"])
    offset_brutto= brutto_font.getlength("brutto "+data["cena brutto"])
    # add text to the image
    nazwa = ImageDraw.Draw(img)
    nazwa.multiline_text((50, 590), data["nazwa"].replace('|', '\n'), font=name_font, fill=(255, 255, 255))
    nazwa.text((img.width - 60 - offset_netto, 590), data["cena netto"], font=netto_font, fill=(255, 255, 255))
    nazwa.text((img.width - 60 - offset_brutto, 680), "brutto " + data["cena brutto"], font=brutto_font, fill=(255, 255, 255))
    return img


def paste_image(element):
    # check if element has "podwojna" attribute, whic means that it takes two colums of size. Assing proper iamges.
    if element["atrybut"].find("podwojna") == -1:
        rama = Image.open("ramka.png", "r")
    else:
        rama = Image.open("ramka_double.png", "r")
    # calculate the maximum height and width of future product image
    width = rama.width - 100
    height = rama.height - 230
    margin = 50
    # load photo
    zdjecie = element["numer zdjecia"]
    temp = Image.new("RGBA", rama.size)
    # change resolution with proper ratio

    fotka = change_resolution(Image.open(zdjecie, "r"), width, height)
    # calculate the center point inside the border
    x = int((margin + width - fotka.width) / 2)
    y = int((margin + height - fotka.height) / 2)
    # combine all the layers and return the photo
    temp.paste(fotka, (x, y))
    final = Image.new("RGBA", rama.size)
    final = Image.alpha_composite(final, rama)
    final = Image.alpha_composite(final, temp)
    return final


# resize the foto to fit area inside the frame, with respect to ratio
def change_resolution(zdjecie, width, height):
    r1 = width / zdjecie.width
    r2 = height / zdjecie.height
    ratio = min(r1, r2)
    width = int(zdjecie.width * ratio)
    height = int(zdjecie.height * ratio)
    return zdjecie.resize((width, height))
