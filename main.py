import rysowanie
import products

# collect data
data = products.read_file("produkty.csv")
# check for errors
errors = products.check_if_images_exists(data, "./Images/")
if len(errors):
    print("Pojawiły się błędy!")
    for error in errors:
        print(f'Nie można znaleźć zdjęcia "{error}"')
    input("Napraw recznie problemy! Pamietam ze przyjmuje tylko png!\n\nPress Enter to continue...")
else:
    # make flyer
    rysowanie.make_flyer(data)

