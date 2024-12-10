from tkinter import *


class Interface:
    """Responsable de la boucle principale du jeu adaptée à l'interface graphique"""
    # taille d'une cellule en pixels
    SIZE = 30

    def __init__(self):
        self.root = Tk()

        # Cache la fenêtre principale au début grâce à withdraw()
        # La fenêtre principale sera affichée après la fermeture de la popup avec deiconify().
        self.root.withdraw()

        # Variable de contrôle pour stocker le nombre de cellules du plateau
        self.__number_var = IntVar()

        # Affiche la popup pour demander la taille du plateau
        self.popup_ask_number()
        # Attendre que la popup soit fermée avant de continuer
        self.root.wait_window(self.__popup_i)

        # Récupérer le nombre de cellules depuis la popup
        self.__n_cells = self.get_number_cells()

        # Afficher la fenêtre principale une fois la popup fermée
        self.root.deiconify()
        self.root.title("Jeu de Plateau")
        # Gestion couleur de la fenêtre principale
        self.root.config(bg="snow3")

        # Initialiser le jeu avec la taille choisie par l'utilisateur (Instanciation Game)
        self.__game_instance = Game(self.__n_cells)
        # Initialisation du board
        self.__game_instance.initialize_board()

        # Création du canvas pour le plateau de jeu, centré avec des marges
        self.__canvas = Canvas(
            self.root,
            width=self.__n_cells * Interface.SIZE,
            height=self.__n_cells * Interface.SIZE,
            background="alice blue",
            highlightthickness=2,
            highlightbackground="black"
        )
        # highlightthickness => l'épaisseur de la bordure (en pixels)
        # highlightbackground => la couleur de la bordure sans focus

        # Définir la taille de la fenêtre principale en fonction du plateau
        self.root.geometry(f"{(self.__n_cells * Interface.SIZE) + 100}x{(self.__n_cells * Interface.SIZE) + 120}")

        # Centrer la fenêtre par rapport à la taille de l'écran de l'utilisateur
        self.center_window()
        self.__canvas.pack(padx=40, pady=30)

        # Définition d'une taille fixe pour chaque cellule
        self.cell_size = Interface.SIZE

        # Label indiquant le joueur actuel
        self.info_lbl_player = Label(
            self.root,
            text=f"Tour du joueur {self.__game_instance.current_player.player_number}",
            font=("Helvetica", 14),
            bg="snow3"
        )
        # le self renvoi à Game, à la variable current_player, qui est un objet de Player, et a pour attribut player-number
        self.info_lbl_player.pack(pady=(0, 20))

        # Variable de contrôle pour la sélection d'un pion au clic
        self.is_click_selection_pawn = BooleanVar()
        # Liaison du clic avec la méthode handle_click
        self.__canvas.bind("<Button-1>", self.handle_click)
        self.update_canvas()

        # Lancement de la boucle principale de Tkinter
        self.root.mainloop()

    def center_window(self):
        """Méthode responsable du positionnement centré selon la taille de l'écran de l'utilisateur"""
        # Méthode qui met à jour les informations de la fenêtre pour obtenir sa taille actuelle.
        self.root.update_idletasks()

        # Largeur actuelle de la fenêtre Tkinter (self.root) en pixels
        width = self.root.winfo_width()
        height = self.root.winfo_height()

        # Récupèrer la largeur total de la fenètre du PC
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def popup_ask_number(self):
        """Méthode pour afficher une popup pour permettre au joueur
        de choisir la taille du plateau entre 6 et 12 cellules."""

        def validation():
            try:
                # Convertit la saisie en entier avec int(), utilisation méthode get()
                number = int(entry_pop.get())
                if 6 <= number <= 12 and number % 2 == 0:
                    # Stocker le nombre dans la variable de contrôle avec la méthode set()
                    self.__number_var.set(number)
                    # Fermer la fenêtre
                    self.__popup_i.destroy()

                else:
                    # Message d'erreur
                    lbl_msg.config(text="Veuillez entrer un \n nombre pair entre 6 et 12.")
            except ValueError:
                lbl_msg.config(text="Entrée invalide, veuillez \n entrer un nombre entier.")

        # création fenêtre popup Tkinter:
        self.__popup_i = Toplevel(self.root)
        self.__popup_i.title("Choisir la taille du plateau")

        # Assurer que la popup soit au-dessus et active
        self.__popup_i.grab_set()
        self.__popup_i.lift()
        self.__popup_i.attributes('-topmost', True)

        lbl_popup_i = Label(
            self.__popup_i,
            text="Veuillez entrer la taille du plateau :\n un nombre de lignes pair entre 6 et 12.",
            font=("Helvetica", 14)
        )

        lbl_popup_i.pack(padx=20, pady=20)
        # Saisie
        entry_pop = Entry(self.__popup_i)
        entry_pop.pack(pady=5)

        lbl_msg = Label(self.__popup_i, text="", fg="red")
        lbl_msg.pack()
        # Le bouton Valider appelle la fonction interne validation
        button_ok = Button(
            self.__popup_i,
            text="Valider",
            font=("helvetica", 12),
            bg="snow3",
            command=validation
        )
        button_ok.pack(pady=(10, 5))

    def get_number_cells(self) -> int :
        """Méthode pour récupérer la taille du plateau après la fermeture de la popup."""
        return self.__number_var.get()

    def update_canvas(self):
        """Mise à jour de l'affichage du plateau de jeu sur le canvas"""
        self.__canvas.delete("all")
        self.draw_grid()
        for i, row in enumerate(self.__game_instance.board):
            for j, cell in enumerate(row):
                self.draw_pawn(i, j, cell)

    def draw_grid(self):
        """Méthode qui dessine le quadrillage du plateau de jeu"""
        size = Interface.SIZE
        rows, cols = self.__n_cells, self.__n_cells
        for i in range(rows):
            # Méthode create_line(x1, y1, x2, y2, options...),
            # (x1, y1) = point de départ de la ligne
            # (x2, y2) = point d'arrivée de la ligne
            # i * cell_size : La ligne commence à une hauteur qui dépend de i et de cell_size. (par exemple, 0 pour la première ligne, 1 pour la deuxième, etc.).
            self.__canvas.create_line(0, i * size, cols * size, i * size, fill="black")
        for j in range(cols):
            self.__canvas.create_line(j * size, 0, j * size, rows * size, fill="black")

    def draw_pawn(self, row_x, col_y, symbol):
        """Méthode qui dessine les pions sur le plateau de jeu (forme, couleur)"""
        size = Interface.SIZE
        padding = 5
        # row_x * size : Détermine la position horizontale du coin gauche de la cellule.
        # (row_x + 1) * size : Calcule le bord droit de la cellule.
        # col_y * size : Détermine la position verticale du coin supérieur de la cellule.
        # (col_y + 1) * size : Calcule le bord inférieur de la cellule.
        x0, y0 = (row_x * size + padding), (col_y * size + padding)
        x1, y1 = ((row_x + 1) * size - padding), ((col_y + 1) * size - padding)

        color_dict = {"Q": "tan1", "o": "firebrick2", "R": "Orchid3", "x": "RoyalBlue4", ".": "alice blue"}
        color = color_dict[symbol]
        self.__canvas.create_oval(x0, y0, x1, y1, fill=color, outline="alice blue")

    def handle_click(self, event):
        """Gérer les clics sur le plateau de jeu pour sélectionner et déplacer les pions"""
        size = Interface.SIZE
        col = event.y // size
        row = event.x // size

        # 1er premier clic, on sélectionne le pion, utilisation variable booléenne is_click_selection_pawn = Not True
        if not self.is_click_selection_pawn.get():
            if (0 <= row < self.__n_cells and 0 <= col < self.__n_cells and
                    self.__game_instance.board[row][col] in [self.__game_instance.current_player.queen_symbol,
                                                             self.__game_instance.current_player.tower_symbol]):

                # Vérifier s'il existe un mouvement possible pour ce pion
                if self.__game_instance.current_player.pawn_choice(row, col):
                    # Mise à jour des coordonées du pion sélectionné
                    self.start_row, self.start_col = row, col
                    # Mise à jours à True grâce à la méthode set()
                    self.is_click_selection_pawn.set(True)
                    self.focus_pawn(row, col)

        # is_click_selection_pawn = True => Il y a déjà eu un clic
        else:
            x_start, y_start = self.start_row, self.start_col
            x_end, y_end = row, col

            if self.__game_instance.current_player.is_possible_move(x_start, y_start, x_end, y_end):
                # Effectuer le mouvement avec game.current_player.move_click
                self.__game_instance.current_player.move_click(x_start, y_start, x_end, y_end)
                self.update_canvas()

                # Vérifier s'il y a une capture après le mouvement.
                if self.__game_instance.board[x_end][y_end] == self.__game_instance.current_player.tower_symbol:
                    # Passage d'une fonction en argument => un callback
                    self.__game_instance.current_player.capture(x_end, y_end, self.update_canvas)

                # Vérifier si game.current_player.is_victory = True
                if self.__game_instance.current_player.is_victory():
                    self.popup_victory(self.__game_instance.current_player.player_number)
                else:
                    # Changer de joueur si pas de victoire
                    self.__game_instance.exchange_player()
                    self.info_lbl_player.config(
                        text=f"Tour du joueur {self.__game_instance.current_player.player_number}")
                self.is_click_selection_pawn.set(False)

    def focus_pawn(self, row_x, col_y):
        """Mettre en évidence un pion sélectionné, par un encerclement vert"""
        padding = 2
        size = Interface.SIZE
        x0, y0 = (row_x * size + padding), (col_y * size + padding)
        x1, y1 = ((row_x + 1) * size - padding), ((col_y + 1) * size - padding)
        self.__canvas.create_oval(x0, y0, x1, y1, outline="green", width=2)

    def popup_victory(self, player_number):
        """Créer une popup pour déclarer la victoire du joueur et proposer une nouvelle partie."""
        # Création popup indépendante de la fenêtre principale = Toplevel(ma fenêtre)
        victory_popup = Toplevel(self.root)
        victory_popup.title("Victoire!")
        # Empêcher les interactions avec la fenêtre principale tant que la popup n'est pas fermée avec grab_set()
        victory_popup.grab_set()
        # Assure que la popup reste visible au-dessus de toutes les autres fenêtres.
        victory_popup.attributes('-topmost', True)
        # Label de la popup
        lbl_victory = Label(
            victory_popup,
            text=f"Le joueur {player_number} a gagné!",
            font=("helvetica", 14)
        )
        lbl_victory.pack(padx=20, pady=20)

        # Création d'un bouton pour rejouer en lanceant la commande
        button_new_game = Button(
            victory_popup,
            text="Nouvelle Partie",
            font=("helvetica", 14),
            bg="PaleGreen1",
            command=self.new_game
        )
        button_new_game.pack(pady=(10, 5))

        # Création d'un bouton pour quitter
        button_quit = Button(
            victory_popup,
            text="Quitter",
            font=("helvetica", 14),
            bg="coral1",
            command=self.root.quit
        )
        button_quit.pack(pady=5)

    def new_game(self):
        """Réinitialiser le jeu pour une nouvelle partie."""
        # Si nouvelle partie, supprime la fenêtre et recrée un objet
        self.root.destroy()
        self.__init__()


class Game:
    """Responsabilities: board, Game play
    => attributs necessaires: nb cellules d'une ligne"""

    def __init__(self, nb_cells):
        # Nombre de cellules d'une rangée
        self.__nb_cells_g = nb_cells
        # Initialisation du plateau vide
        self.board = [["."] * self.__nb_cells_g for _ in range(self.__nb_cells_g)]
        # Créer deux joueurs
        self.player1 = Player(1, self.board)
        self.player2 = Player(2, self.board)
        # Au départ le joueur courant est le joueur 1
        self.current_player = self.player1

    def initialize_board(self):
        """Méthode qui initialise le plateau de départ."""
        n = self.__nb_cells_g
        # Placement des pièces du player 1:
        for i in range(n // 2):
            for j in range(n // 2, n):
                self.board[i][j] = "x"
        # placement en dernier, écrase une tour
        self.board[0][n - 1] = "R"

        # Placement des pièces du player 2:
        for i in range(n // 2, n):
            for j in range(n // 2):
                self.board[i][j] = "o"
        self.board[n - 1][0] = "Q"

    def exchange_player(self):
        """Méthode qui change le joueur actif après chaque tour."""
        # joueur actif = joueur 1 si joueur_actuel == joueur 2 sinon => joueur actif = joueur 2
        self.current_player = self.player1 if self.current_player == self.player2 else self.player2


class Player:
    """Classe responsable des choix du joueur, de la capture et de la victoire"""

    def __init__(self, player_number, board):
        self.player_number = player_number

        # attributs variables selon la valeur player_number
        # (pas self car ce n'est pas un attribut que je veux mais une valeur)
        self.queen_symbol = "R" if player_number == 1 else "Q"
        self.tower_symbol = "x" if player_number == 1 else "o"
        self.empty_symbol = "."

        self.board = board

        # Nombre total de pions au départ
        self.pawn_pl1 = (len(board) // 2) ** 2
        self.pawn_pl2 = (len(board) // 2) ** 2
        self.__pawn_remain_opponent = self.pawn_pl1 if player_number == 2 else self.pawn_pl2
        self.__queen_pos = (0, len(board) - 1) if player_number == 1 else (len(board) - 1, 0)

    def pawn_choice(self, row, col) -> bool:
        """Vérifie s'il existe un mouvement possible pour le pion à la position (row, col)."""
        possible_moves_tower = [
            (row - 1, col), (row + 1, col),                # Haut et Bas
            (row, col - 1), (row, col + 1)                 # Gauche et Droite
        ]
        possible_moves_queen = possible_moves_tower + [
            (row - 1, col - 1), (row - 1, col + 1),        # Diagonales Haut-Gauche et Haut-Droite
            (row + 1, col - 1), (row + 1, col + 1)         # Diagonales Bas-Gauche et Bas-Droite
        ]

        if self.board[row][col] == self.queen_symbol:
            # Vérifier chaque mouvement possible
            for x_end, y_end in possible_moves_queen:
                if (0 <= x_end < len(self.board) and 0 <= y_end < len(self.board) and
                        self.is_possible_move(row, col, x_end, y_end)):
                    return True

        elif self.board[row][col] == self.tower_symbol:
            # Vérifier chaque mouvement possible
            for x_end, y_end in possible_moves_tower:
                if (0 <= x_end < len(self.board) and 0 <= y_end < len(self.board) and
                        self.is_possible_move(row, col, x_end, y_end)):
                    return True

        return False

    def is_possible_move(self, x_start, y_start, x_end, y_end) -> bool:
        """Méthode qui valide si le chemin est libre et valide le mouvement choisi."""

        # Vérifier si les coordonnées de départ sont valides
        if not (0 <= x_start < len(self.board) and 0 <= y_start < len(self.board)):
            return False

        # Vérifier si la case d'arrivée est valide et vide
        if not (0 <= x_end < len(self.board) and 0 <= y_end < len(self.board)):
            return False
        if self.board[x_end][y_end] != self.empty_symbol:
            return False

        pawn = self.board[x_start][y_start]
        path = ()

        # Vérifier le type de pion et crée un liste des pions au sein de ce déplacement
        if pawn == self.queen_symbol:
            if x_start != x_end and y_start != y_end:
                path = Pawn(self.board).diagonal_move(x_start, x_end, y_start, y_end)
            else:
                path = Pawn(self.board).straight_move(x_start, x_end, y_start, y_end)

        elif pawn == self.tower_symbol:
            path = Pawn(self.board).straight_move(x_start, x_end, y_start, y_end)

        # Contrôlé que path contient uniquement le symbole des cases vides
        if all(cells == self.empty_symbol for cells in path):
            return True
        return False

    def move_click(self, x_start, y_start, x_end, y_end):
        """Méthode qui effectue le mouvement en déplaçant le pion."""

        # Effectuer le mouvement en échangeant les valeurs et mise à vide ancienne case
        self.board[x_end][y_end] = self.board[x_start][y_start]
        self.board[x_start][y_start] = self.empty_symbol

        # Si c'est la reine qui est déplacée => mise à jour de ses coordonnées
        if self.board[x_end][y_end] == self.queen_symbol:
            self.__queen_pos = (x_end, y_end)

    def is_capture(self, x_end, y_end) -> bool:
        """Méthode qui vérifie si une capture est possible après le déplacement d'une tour."""

        # Récupère la position de la reine du joueur actif mise à jour
        queen_x, queen_y = self.__queen_pos

        # if = True => diagonale
        if x_end != queen_x and y_end != queen_y:

            # Variable qui représente le pion adverse pour les comparaisons:
            tower_opponent = "o" if self.player_number == 1 else "x"

            # Calculer les coordonnées des autres sommets avec les coordonnées connues
            # la coordonnée x de la reine et y du pion déplacé et inversement
            rect_x1, rect_y1 = queen_x, y_end                         # angle A
            rect_x2, rect_y2 = x_end, queen_y                         # angle B

            capture = 0

            # Vérifie que les angles sont bien à l'intérieur du board et contiennent une tour adverse
            if (0 <= rect_x1 < len(self.board) and 0 <= rect_y1 < len(self.board) and
                    self.board[rect_x1][rect_y1] == tower_opponent):  # angle A
                capture += 1
            if (0 <= rect_x2 < len(self.board) and 0 <= rect_y2 < len(self.board) and
                    self.board[rect_x2][rect_y2] == tower_opponent):  # angle B
                capture += 1

            # if is_capture > 0 => True
            return capture > 0
        return False

    def capture(self, x_end, y_end, canvas_update_callback):
        """Méthode qui capture une pièce adverse si les conditions sont remplies.
        Utilise la méthode is_capture pour vérifier si la capture est possible.
        Utilise un callback => une fonction qui pourra être appellée dans la méthode
        Appelée après un déplacement pour gérer la capture et mettre à jour le canvas graphique."""

        if self.is_capture(x_end, y_end):

            # Récupère la position de la reine du joueur actif mise à jour dans move si besoin
            queen_x, queen_y = self.__queen_pos

            # Crée une variable qui représente le pion adverse pour les comparaisons:
            tower_opponent = "o" if self.player_number == 1 else "x"

            # Calculer les coordonnées des autres sommets avec les coordonnées connues
            # le x de la reine et le y du pion déplacé et inversement
            rect_x1, rect_y1 = queen_x, y_end  # angle A
            rect_x2, rect_y2 = x_end, queen_y  # angle B

            # angle A
            if self.board[rect_x1][rect_y1] == tower_opponent:
                self.board[rect_x1][rect_y1] = self.empty_symbol
                self.__pawn_remain_opponent -= 1
            # angle B
            if self.board[rect_x2][rect_y2] == tower_opponent:
                self.board[rect_x2][rect_y2] = self.empty_symbol
                self.__pawn_remain_opponent -= 1

            # Appel de la mise à jour de l'interface graphique après chaque capture
            canvas_update_callback()

    def is_victory(self) -> bool:
        """Méthode qui vérifie le nombre de pièces restantes"""
        return self.__pawn_remain_opponent <= 2


class Pawn:
    """Méthode qui est responsable des pions et des règles de mouvements"""

    def __init__(self, board):
        self.__board = board

    def straight_move(self, x_start, x_end, y_start, y_end) -> list:
        """Méthode de mouvement en ligne droite"""
        # Mouvement vertical
        if x_start != x_end and y_start == y_end:
            step = 1 if x_end > x_start else -1
            return [self.__board[x][y_start] for x in range(x_start + step, x_end, step)]

        # Mouvement horizontal
        elif y_start != y_end and x_start == x_end:
            step = 1 if y_end > y_start else -1
            return [self.__board[x_start][y] for y in range(y_start + step, y_end, step)]

    def diagonal_move(self, x_start, x_end, y_start, y_end) -> list:
        """Mouvement en diagonale"""
        if abs(x_start - x_end) == abs(y_start - y_end):
            # Sens de déplacement: vers le haut/droite (1) ou bas/gauche (-1)
            step_x = 1 if x_end > x_start else -1
            step_y = 1 if y_end > y_start else -1
            # Commence à 1 pour retirer la position de départ (x_start, y_start), la position d'arrivée (x_end, y_end) exclus
            return [self.__board[x_start + i * step_x][y_start + i * step_y] for i in range(1, abs(x_end - x_start))]


window = Interface()
