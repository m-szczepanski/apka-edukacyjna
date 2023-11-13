import tkinter as tk
from tkinter import PhotoImage
from app.functions.distribute_session_data import distribute_data_json
import random


class LearningSession(tk.Toplevel):
    def __init__(self, session):
        super().__init__()
        self.learning_session = session
        self.title(f"Session: {self.learning_session}")
        self.geometry("681x686")
        self.resizable(False, False)
        self.wm_attributes("-topmost", True)

        self.frames = {}

        (self.flashcard_dict, self.match_expression_dict, self.match_translation_dict, self.tf_dict, self.pick_dict,
         self.hangman_dict) = distribute_data_json(self.learning_session)
        # debug
        print("flashcard: ", self.flashcard_dict)
        print("match_expression: ", self.match_expression_dict)
        print("match_translation: ", self.match_translation_dict)
        print("tf: ", self.tf_dict)
        print("pick: ", self.pick_dict)
        print("hangman: ", self.hangman_dict)

        self.chosen_dict, self.dict_name = self.random_dict()
        print("dict name: ", self.dict_name)

        key, value = self.get_random_key_value()

        self.frames["flashcard"] = Flashcard(self, key, value)
        self.frames["match_expression"] = MatchExpression(self, key, value)
        self.frames["match_translation"] = MatchTranslation(self, key, value)
        self.frames["tf"] = TrueFalse(self, key, value)
        self.frames["pick"] = PickCorrect(self, key, value)
        self.frames["hangman"] = Hangman(self, key, value)

        self.show_frame(self.dict_name)

    def show_frame(self, frame_name):
        if frame := self.frames.get(frame_name):
            frame.tkraise()

            for name, other_frame in self.frames.items():
                if name != frame_name:
                    other_frame.forget()

    def random_dict(self, consecutive_limit=3):
        dict_choices = [
            ("flashcard", self.flashcard_dict),
            ("match_expression", self.match_expression_dict),
            ("match_translation", self.match_translation_dict),
            ("tf", self.tf_dict),
            ("pick", self.pick_dict),
            ("hangman", self.hangman_dict),
        ]

        available_dicts = [(name, dictionary) for name, dictionary in dict_choices if len(dictionary) > 0]

        if not available_dicts:
            return None, None

        chosen_entry = None
        for _ in range(consecutive_limit):
            chosen_entry = random.choice(available_dicts)
            if chosen_entry != getattr(self, f"last_chosen_{chosen_entry[0]}", None):
                break

        setattr(self, f"last_chosen_{chosen_entry[0]}", chosen_entry[0])

        return chosen_entry[1], chosen_entry[0]

    def get_random_key_value(self):
        if not self.chosen_dict:
            return None, None

        random_key = random.choice(list(self.chosen_dict.keys()))
        random_value = self.chosen_dict[random_key]
        return random_key, random_value


class Flashcard(tk.Frame):
    def __init__(self, parent, key, value):
        super().__init__(parent)
        self.key = key
        self.value = value
        self.configure(width=681, height=686)

        self.background_image = PhotoImage(file=
                                           "./components/graphical_components/flashcard/flashcard_panel.png")
        self.background = tk.Label(self, image=self.background_image)
        self.background.place(relwidth=1, relheight=1)
        self.pack()

        self.flashcard_front_bg = PhotoImage(file="./components/graphical_components/flashcard/flashcard_front.png")
        self.flashcard_back_bg = PhotoImage(file="./components/graphical_components/flashcard/flashcard_back.png")
        self.flip_button_bg = PhotoImage(file="./components/graphical_components/flashcard/flip_button.png")
        self.canvas_background = PhotoImage(file="./components/graphical_components/flashcard/canvas_bg.png")
        self.yes_button_bg = PhotoImage(file="./components/graphical_components/flashcard/yes_button.png")
        self.no_button_bg = PhotoImage(file="./components/graphical_components/flashcard/no_button.png")

        self.canvas = tk.Canvas(self, width=616, height=311, bg="#9ed2be", highlightthickness=0)
        self.canvas_bg = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.flashcard_front_bg)
        self.card_language = self.canvas.create_text(300, 50, text="Language", font=("Inter", 30, "normal"),
                                                     fill="#FFD9B7")
        self.card_word = self.canvas.create_text(300, 163, text="word", font=("Inter", 70, "bold"), fill="#FFFFFF")
        self.canvas.place(x=32, y=62)

        self.flip_button = tk.Button(self, image=self.flip_button_bg, command=self.test, bd=0, bg="#9ED2BE")
        self.flip_button.place(x=248, y=398)

        self.unknown_button = tk.Button(self, image=self.no_button_bg, command=lambda: self.test(),
                                        bd=0, bg="#9ED2BE")
        self.unknown_button.place(x=82, y=488)

        self.known_button = tk.Button(self, image=self.yes_button_bg, command=self.test, bd=0, bg="#9ED2BE")
        self.known_button.place(x=448, y=488)

        self.current_card = {}
        self.unknown = {}

        print(self.key, self.value)

    def test(self):
        pass


class MatchExpression(tk.Frame):
    def __init__(self, parent, key, value):
        super().__init__(parent)
        self.key = key
        self.value = value
        self.configure(width=681, height=686)

        self.background_image = PhotoImage(file="./components/graphical_components/games/match_expression/"
                                           "match_expression_bg.png")
        self.background = tk.Label(self, image=self.background_image)
        self.background.place(relwidth=1, relheight=1)
        self.pack()


class MatchTranslation(tk.Frame):
    def __init__(self, parent, key, value):
        super().__init__(parent)
        self.key = key
        self.value = value
        self.value = value
        self.configure(width=681, height=686)

        self.background_image = PhotoImage(file=
                                           "./components/graphical_components/games/match_translation/"
                                           "match_translation_bg.png")
        self.background = tk.Label(self, image=self.background_image)
        self.background.place(relwidth=1, relheight=1)
        self.pack()


class TrueFalse(tk.Frame):
    def __init__(self, parent, key, value):
        super().__init__(parent)
        self.key = key
        self.value = value
        self.configure(width=681, height=686)

        self.background_image = PhotoImage(file=
                                           "./components/graphical_components/games/true_false/true_false_bg.png")
        self.background = tk.Label(self, image=self.background_image)
        self.background.place(relwidth=1, relheight=1)
        self.pack()


class PickCorrect(tk.Frame):
    def __init__(self, parent, key, value):
        super().__init__(parent)
        self.key = key
        self.value = value
        self.configure(width=681, height=686)

        self.background_image = PhotoImage(file=
                                           "./components/graphical_components/games/pick_correct/pick_correct_bg.png")
        self.background = tk.Label(self, image=self.background_image)
        self.background.place(relwidth=1, relheight=1)
        self.pack()


class Hangman(tk.Frame):
    def __init__(self, parent, key, value):
        super().__init__(parent)
        self.key = key
        self.value = value
        self.configure(width=681, height=686)

        self.background_image = PhotoImage(file=
                                           "./components/graphical_components/games/hangman/hangman_bg.png")
        self.background = tk.Label(self, image=self.background_image)
        self.background.place(relwidth=1, relheight=1)
        self.pack()
