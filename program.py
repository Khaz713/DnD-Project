from actors import Player


def main():
    while True:
        name = input('Enter the name of your character: ')
        choice = eval(input('Select your class: \n1.Rogue\n'))
        if choice == 1:
            player = Rogue(name)
            break
        else:
            print('Incorrect value, please try again')

    print(f'{player.hit_roll()[0]} {player.hit_roll()[1]}')
    print(player.damage_roll(False))
    print(player.damage_roll(True))


if __name__ == '__main__':
    main()
