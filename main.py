import json
import os



class Player:
    def __init__(self, nume, hp, attack, gold, xp, level):
        self.nume = nume
        self.hp = hp
        self.attack = attack
        self.gold = gold
        self.xp = xp
        self.level = level

    def afiseaza_status(self):
        print("\n===== 📊 STATUS PLAYER =====")
        print(f"🧙 Nume: {self.nume}")
        print(f"❤️ HP: {self.hp}/100")
        print(f"⚔️ Attack: {self.attack}")
        print(f"🪙 Gold: {self.gold}")
        print(f"⭐ XP: {self.xp}/100")
        print(f"🏆 Level: {self.level}")

    def ataca(self, inamic):
        print(f"\n⚔️ {self.nume} îl atacă pe {inamic.nume}!")
        inamic.hp -= self.attack

        if inamic.hp <= 0:
            inamic.hp = 0
            print(f"💀 {inamic.nume} a fost învins!")
        else:
            print(f"❤️ {inamic.nume} mai are {inamic.hp} HP.")



class Inamic:
    def __init__(self, nume, hp, attack):
        self.nume = nume
        self.hp = hp
        self.attack = attack

    def afiseaza_status(self):
        print(
            f"👹 {self.nume} | "
            f"❤️ HP: {self.hp} | "
            f"⚔️ Attack: {self.attack}"
        )

    def ataca(self, player):
        print(f"\n👹 {self.nume} îl atacă pe {player.nume}!")
        player.hp -= self.attack

        if player.hp <= 0:
            player.hp = 0
            print(f"💀 {player.nume} a fost învins!")
        else:
            print(f"❤️ Ai rămas cu {player.hp} HP.")



def salveaza_joc(player):
    date = {
        "nume": player.nume,
        "hp": player.hp,
        "attack": player.attack,
        "gold": player.gold,
        "xp": player.xp,
        "level": player.level
    }

    with open("jocuri.json", "w", encoding="utf-8") as f:
        json.dump(date, f, indent=4, ensure_ascii=False)

    print("\n💾 Jocul a fost salvat cu succes!")



def incarca_joc():
    if not os.path.exists("jocuri.json"):
        print("\n❌ Nu există niciun joc salvat!")
        return None

    try:
        with open("jocuri.json", "r", encoding="utf-8") as f:
            date = json.load(f)

        player = Player(
            date["nume"],
            date["hp"],
            date["attack"],
            date["gold"],
            date["xp"],
            date["level"]
        )

        print("\n📂 Jocul a fost încărcat cu succes!")
        return player

    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        print("\n❌ Fișierul de salvare este invalid!")
        return None



def verifica_level_up(player):
    while player.xp >= 100:
        player.xp -= 100
        player.level += 1
        player.attack += 5

        print(f"\n🏆 LEVEL UP! Ai ajuns la nivelul {player.level}!")
        print(f"⚔️ Attack crescut la {player.attack}!")



def lupta(player):
    print("\n===== 👹 ALEGE INAMICUL =====")
    print("1. 👺 Goblin — 60 HP")
    print("2. 🐺 Wolf — 80 HP")
    print("3. 👹 Orc — 120 HP")

    alegere_inamic = input("👉 Alege inamicul: ")

    if alegere_inamic == "1":
        inamic = Inamic("Goblin", 60, 10)
        gold_primit = 25
        xp_primit = 15

    elif alegere_inamic == "2":
        inamic = Inamic("Wolf", 80, 15)
        gold_primit = 40
        xp_primit = 25

    elif alegere_inamic == "3":
        inamic = Inamic("Orc", 120, 20)
        gold_primit = 60
        xp_primit = 40

    else:
        print("❌ Alegere invalidă!")
        return

    print("\n===== ⚔️ LUPTA A ÎNCEPUT! ⚔️ =====")
    player.afiseaza_status()
    inamic.afiseaza_status()

    while True:
        print("\n⚔️ Ce vrei să faci?")
        print("1. Atacă")
        print("2. Vezi status")
        print("3. Fugi")

        alegere = input("👉 Alege: ")

        if alegere == "1":
            player.ataca(inamic)

            if inamic.hp <= 0:
                print("\n🎉 Ai câștigat lupta!")

                player.gold += gold_primit
                player.xp += xp_primit

                print(f"🪙 Ai primit {gold_primit} Gold!")
                print(f"⭐ Ai primit {xp_primit} XP!")

                verifica_level_up(player)
                break

            inamic.ataca(player)

            if player.hp <= 0:
                print("\n💀 Ai pierdut lupta!")
                print("❤️ Ai fost readus la 100 HP!")

                player.hp = 100
                break

        elif alegere == "2":
            player.afiseaza_status()
            inamic.afiseaza_status()

        elif alegere == "3":
            print("\n🏃 Ai fugit din luptă!")
            break

        else:
            print("❌ Alegere invalidă!")



def shop(player):
    while True:
        print("\n===== 🛒 SHOP =====")
        print(f"🪙 Gold disponibil: {player.gold}")
        print(f"❤️ HP actual: {player.hp}/100")
        print("1. ⚔️ +5 Attack — 25 Gold")
        print("2. 🧪 +30 HP — 20 Gold")
        print("3. 🚪 Înapoi la meniu")

        alegere = input("👉 Alege: ")

        if alegere == "1":
            if player.gold >= 25:
                player.gold -= 25
                player.attack += 5

                print("\n✅ Upgrade cumpărat cu succes!")
                print(f"⚔️ Attack actual: {player.attack}")
                print(f"🪙 Gold rămas: {player.gold}")
            else:
                print("❌ Nu ai suficient Gold!")

        elif alegere == "2":
            if player.hp >= 100:
                print("❤️ Ai deja viața maximă!")

            elif player.gold >= 20:
                player.gold -= 20
                player.hp = min(player.hp + 30, 100)

                print("\n✅ Poțiune cumpărată cu succes!")
                print(f"❤️ HP actual: {player.hp}")
                print(f"🪙 Gold rămas: {player.gold}")

            else:
                print("❌ Nu ai suficient Gold!")

        elif alegere == "3":
            print("🚪 Te-ai întors la meniul principal!")
            break

        else:
            print("❌ Alegere invalidă!")




def main():
    player = Player("Player1", 100, 20, 0, 0, 1)

    while True:
        print("\n===== ⚔️ GAME BATTLE ARENA ⚔️ =====")
        print("1. Luptă 👹")
        print("2. Shop 🛒")
        print("3. Status 📊")
        print("4. Save Game 💾")
        print("5. Load Game 📂")
        print("6. Ieșire 🚪")

        alegere_meniu = input("👉 Alege: ")

        if alegere_meniu == "1":
            lupta(player)

        elif alegere_meniu == "2":
            shop(player)

        elif alegere_meniu == "3":
            player.afiseaza_status()

        elif alegere_meniu == "4":
            salveaza_joc(player)

        elif alegere_meniu == "5":
            player_incarcat = incarca_joc()

            if player_incarcat is not None:
                player = player_incarcat

        elif alegere_meniu == "6":
            print("\n👋 Mulțumesc că ai jucat Game Battle Arena!")
            break

        else:
            print("❌ Alegere invalidă!")
            
if __name__ == "__main__":
    main()