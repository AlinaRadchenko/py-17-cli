import random
import subprocess
import time
import json

def main():
    name = show_intro()
    show_rules()
    main_menu(name)



def show_intro():
    while True:
        name = input("Як тебе звати? ").strip().title()
        if name:
            break
        print("Ім'я не може бути порожнім. Спробуй ще раз.")

    print("╔════════════════════════════════════╗\n"
          "║            THE N-DOORS             ║\n"
          "╠════════════════════════════════════╣\n"
          "║        [ UNKNOWN MESSAGE ]         ║\n"
          "║                                    ║\n"
         f"║{(name + ', перед тобою двері').center(36)}║\n"
          "║ За кожною приховане випробування.  ║\n"
          "║        У тебе є три життя.         ║\n"
          "║                                    ║\n"
          "║ Чи вистачить їх, щоб знайти вихід? ║\n"
          "║                                    ║\n"
          "║          [ END MESSAGE ]           ║\n"
          "╚════════════════════════════════════╝")
    input("Натисни Enter, щоб продовжити...")
    return name


def show_rules():
    print("╔══════════════════════════════════════════╗\n"
          "║             GAME RULES                   ║\n"
          "╠══════════════════════════════════════════╣\n"
          "║      [ ТВОЇ ЖИТТЯ: ♥  ♥  ♥ ]             ║\n"
          "║                                          ║\n"
          "║ 01. На тебе чекають 4 випробування.      ║\n"
          "║ 02. За кожну невдачу втрачаєш одне життя.║\n"
          "║ 03. Після будь-якої спроби двері         ║\n"
          "║     зачиняються.                         ║\n"
          "║ 04. Якщо життя залишилися -              ║\n"
          "║     можеш обрати інші двері.             ║\n"
          "║ 05. Пройшов 3 або 4 випробування -       ║\n"
          "║     ПЕРЕМОГА!                            ║\n"
          "║ 06. Пройшов менше 3 - ПОРАЗКА.           ║\n"
          "║                                          ║\n"
          "╠══════════════════════════════════════════╣\n"
          "║           [ ENTER TO CONTINUE ]          ║\n"
          "╚══════════════════════════════════════════╝")
    input("Натисни Enter, щоб продовжити...")


def main_menu(name):
    while True:
        print("╔════════════════════════════════════╗\n"
              "║             THE N-DOORS            ║\n"
              "╠════════════════════════════════════╣\n"
              "║                                    ║\n"
              "║       [1] PLAY                     ║\n"
              "║       [2] SCORES                   ║\n"
              "║       [3] HELP                     ║\n"
              "║       [4] QUIT                     ║\n"
              "║                                    ║\n"
              "╚════════════════════════════════════╝")
        choice_user = input("Твій вибір: ").strip()
        if choice_user == "1":
            start_game(name)
        elif choice_user =="2":
            show_scores()
        elif choice_user == "3":
            show_rules()
        elif choice_user == "4":
            break
        else:
            print("Невідома команда. Спробуй ще раз.")


def start_game(name):
    game_dict = {"name": name,
                 "lives": 3,
                 "completed_trials": 0,
                 "status": 	"in_progress",
                 "visited_doors": set()}
    while game_dict["lives"] > 0 and len(game_dict["visited_doors"]) < 4:
        progress = f"Пройдено випробувань: {game_dict['completed_trials']} / 4"
        lives_text = f"Твої життя: {'♥ ' * game_dict['lives']}".strip()
        print( "╔════════════════════════════════════╗\n"
               "║           CURRENT STATUS           ║\n"
               "╠════════════════════════════════════╣\n"
               "║                                    ║\n"
              f"║{progress.center(36)}║\n"
              f"║{lives_text.center(36)}║\n"
               "║                                    ║\n"
               "╠════════════════════════════════════╣\n"
               "║            CHOOSE A DOOR           ║\n"
               "║                                    ║\n"
               "║       ┌──────┐       ┌──────┐      ║\n"
               "║       │  1   │       │  2   │      ║\n"
               "║       │      │       │      │      ║\n"
               "║       └──────┘       └──────┘      ║\n"
               "║                                    ║\n"
               "║       ┌──────┐       ┌──────┐      ║\n"
               "║       │  3   │       │  4   │      ║\n"
               "║       │      │       │      │      ║\n"
               "║       └──────┘       └──────┘      ║\n"
               "║                                    ║\n"
               "╚════════════════════════════════════╝")
        choice_door = input("Обери двері (1–4):  ").strip()
        if choice_door not in game_dict["visited_doors"] and choice_door in ["1", "2", "3", "4"]:
            game_dict["visited_doors"].add(choice_door)
            if choice_door == "1":
                result = door_1()
                if result:
                    game_dict["completed_trials"] += 1
                else:
                    game_dict["lives"] -= 1

            elif choice_door == "2":
                result = door_2()
                if result:
                    game_dict["completed_trials"] += 1
                else:
                    game_dict["lives"] -= 1

            elif choice_door == "3":
                result = door_3()
                if result:
                    game_dict["completed_trials"] += 1
                else:
                    game_dict["lives"] -= 1

            elif choice_door == "4":
                result = door_4()
                if result:
                    game_dict["completed_trials"] += 1
                else:
                    game_dict["lives"] -= 1

        elif choice_door in game_dict["visited_doors"]:
            print("Двері зачинені!")
        else:
            print("Такої двері поки що немає")

    if game_dict["completed_trials"] >= 3 :
        game_dict["status"] = "won"
        print("🏆 YOU WIN!")
    else:
        game_dict["status"] = "lost"
        print("💔 GAME OVER")

    result = {"name": game_dict["name"],
              "status": game_dict["status"],
              "completed_trials": game_dict["completed_trials"]}
    scores = load_scores()
    scores.append(result)
    save_scores(scores)


def door_1():
    right_answer = [6, 16]
    answer_user = []
    numbers_1 = list(range(2, 12, 2))
    numbers_1[2] = "*"
    for i in numbers_1:
        print(i, end=" ")
    while True:
        try:
            answer = int(input("\nТвоя відповідь: "))
        except ValueError:
            print("Ви ввели не число")
        else:
            break
    answer_user.append(answer)

    numbers_2 = [i ** 2 for i in range(2, 7)]
    numbers_2[2] = "*"
    for i in numbers_2:
        print(i, end=" ")
    while True:
        try:
            answer = int(input("\nТвоя відповідь: "))
        except ValueError:
            print("Ви ввели не число")
        else:
            break
    answer_user.append(answer)

    if right_answer == answer_user:
        print("Двері пройдені!")
        return True
    else:
        print("Двері не пройдені!")
        return False


def door_2():
    code_dict = {"☾": "К", "☆": "М", "♧": "А", "◇": "Л", "△": "Ю", "♡": "Н", "□": "Ч"}
    code = "☾ ◇ △ □".split()
    decoding = ""
    for i in code:
        decoding += code_dict[i]


    print(f"╔══════════════════════════════════════════╗\n"
           "║           THE VANISHING CODE             ║\n"
           "║                                          ║\n"
           "║  На стіні ти знаходиш дивне повідомлення.║\n"
           "║  Схоже, його було зашифровано.           ║\n"
           "╠══════════════════════════════════════════╣\n"
           "║  Скористайся таблицею, щоб розшифрувати  ║\n"
           "║  повідомлення.                           ║\n"
           "╠══════════════════════════════════════════╣\n"
           "║       ☾  →  К          ☆  →  М           ║\n"
           "║       ♧  →  А          ◇  →  Л           ║\n"
           "║       △  →  Ю          ♡  →  Н           ║\n"
           "║       □  →  Ч                            ║\n"
           "╠══════════════════════════════════════════╣\n"
           "║                                          ║\n"
          f"║               {" ".join(code)}                    ║\n"
           "║                                          ║\n"
           "╚══════════════════════════════════════════╝\n")

    while True:
        answer = input("Ваш варіант: ").strip().upper()
        if not answer.isalpha():
            print("Потрібно ввести слово")
        else:
            break
    if answer == decoding:
        print("Двері пройдені!")
        return True
    else:
        print("Двері не пройдені!")
        return False

def door_3():
    right_color = "синя"
    available_colors = {"синя", "червона", "жовта"}

    print(f"╔══════════════════════════════════════════╗\n"
          "║              THREE CANDLES               ║\n"
          "╠══════════════════════════════════════════╣\n"
          "║       На столі горять три свічки.        ║\n"
          "║                                          ║\n"
          "║       Усі свічки мають однакову          ║\n"
          "║       довжину — 6 сантиметрів.           ║\n"
          "║       Їх запалили одночасно.             ║\n"
          "╠══════════════════════════════════════════╣\n"
          "║          🔵        🔴        🟡          ║\n"
          "║          🕯️        🕯️        🕯️          ║\n"
          "║                                          ║\n"
          "║       1 см/год   2 см/год   3 см/год     ║\n"
          "║                                          ║\n"
          "║        Яка свічка горітиме найдовше?     ║\n"
          "║                                          ║\n"
          "╚══════════════════════════════════════════╝\n")

    while True:
        answer = input("Твій вибір: ").strip().lower()
        if answer not in available_colors:
            print("Потрібно ввести існуючий колір.")
        else:
            break
    if answer == right_color:
        print("Останнє світло збережено!")
        return True
    else:
        print("Світло згасло...")
        return False

def door_4():

    number_list = [random.randint(1, 15) for i in range(5)]
    print("╔══════════════════════════════════╗\n"
          "║          THE SAFE PATH           ║\n"
          "║           MEMORY TEST            ║\n"
          "╠══════════════════════════════════╣\n"
          "║   Запам'ятай послідовність.      ║\n"
          "║   Через 3 секунди вона зникне.   ║\n"
          "╚══════════════════════════════════╝\n")
    input("Натисни Enter, щоб продовжити...")
    print("╔══════════════════════════════════╗\n"
          f"║{'·'.join(str(i) for i in number_list).center(34)}║\n"
          "╚══════════════════════════════════╝\n")

    time.sleep(3)
    subprocess.run(["clear"])
    fixed_list = number_list.copy()
    missing_index = random.randrange(len(fixed_list))
    correct_answer = fixed_list[missing_index]
    fixed_list[missing_index] = "*"
    print("╔══════════════════════════════════╗\n"
          f"║{'·'.join(str(i) for i in fixed_list).center(34)}║\n"
          "╚══════════════════════════════════╝\n")

    while True:
        try:
            answer = int(input("Яке число зникло: "))
        except ValueError:
            print("Ви ввели не число")
        else:
            break
    if answer == correct_answer:
        print("Гарна памʼять!")
        return True
    else:
        print("Не вірно!")
        return False

def load_scores():
    try:
        with open('scores.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("Scores file not found.")
        return []
    return data

def save_scores(scores):
    with open('scores.json', 'w', encoding="utf-8") as file:
        json.dump(scores,  file,  ensure_ascii=False)

def show_scores():
    scores = load_scores()
    if not scores:
        print("Поки що немає результатів.")
    else:
        for score in scores:
            print(f"{score['name']}: {score['completed_trials']}, {score['status']}")

if __name__ == "__main__":
    main()