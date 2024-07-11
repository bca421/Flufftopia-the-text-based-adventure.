from enemies import enemies
from events import events
from dev_privileges import grant_dev_privileges
from locations import locations
from bosses import bosses  # Added bosses import
import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown

class FlufftopiaApp(App):
    def build(self):
        self.player = self.player_setup()
        self.location_index = 0
        self.current_enemy = None
        self.current_boss = None
        self.unlocked_locations = ["village","enchanted_forest","ancient_ruins"]

        self.main_layout = BoxLayout(orientation='vertical')

        self.health_bar = ProgressBar(max=100, value=self.player['health'])
        self.main_layout.add_widget(self.health_bar)

        self.info_label = Label(text="Welcome to Flufftopia!", size_hint_y=None, height=200)
        self.scroll_view = ScrollView(size_hint=(1, None), size=(400, 400))
        self.scroll_view.add_widget(self.info_label)
        self.main_layout.add_widget(self.scroll_view)

        self.inventory_label = Label(text="Inventory: " + ', '.join(self.player['inventory']))
        self.main_layout.add_widget(self.inventory_label)

        button_layout = GridLayout(cols=6, size_hint_y=None, height=50)
        self.main_layout.add_widget(button_layout)

        self.next_button = Button(text="Next")
        self.next_button.bind(on_press=self.next_location)
        button_layout.add_widget(self.next_button)

        self.skill_button = Button(text="Use Skill")
        self.skill_button.bind(on_press=self.show_skill_popup)
        button_layout.add_widget(self.skill_button)

        self.attack_button = Button(text="Attack")
        self.attack_button.bind(on_press=self.attack_enemy)
        button_layout.add_widget(self.attack_button)

        self.defend_button = Button(text="Defend")
        self.defend_button.bind(on_press=self.defend)
        button_layout.add_widget(self.defend_button)

        self.run_button = Button(text="Run")
        self.run_button.bind(on_press=self.run_from_combat)
        button_layout.add_widget(self.run_button)

        self.explore_button = Button(text="Explore")
        self.explore_button.bind(on_press=self.explore_area)
        button_layout.add_widget(self.explore_button)

        self.enable_combat_buttons(False)  # Disable combat buttons initially

        self.class_selection_popup()

        return self.main_layout

    

    def class_selection_popup(self):
        layout = BoxLayout(orientation='vertical')
        classes = ['Warrior', 'Mage', 'Rogue']
        dropdown = DropDown()

        for cls in classes:
            btn = Button(text=cls, size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)

        class_button = Button(text='Choose Class', size_hint=(1, 0.5))
        class_button.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(class_button, 'text', x))

        submit_button = Button(text='Submit', size_hint=(1, 0.5))
        submit_button.bind(on_press=lambda instance: self.set_player_class(class_button.text))

        layout.add_widget(class_button)
        layout.add_widget(submit_button)

        self.popup = Popup(title='Choose Class', content=layout, size_hint=(0.5, 0.3), auto_dismiss=False)
        self.popup.open()

    def set_player_class(self, player_class):
        self.player['class'] = player_class
        if player_class == 'Warrior':
            self.player.update({'strength': 20, 'defense': 15, 'agility': 5, 'skills': ['Slash', 'Shield Bash']})
        elif player_class == 'Mage':
            self.player.update({'strength': 15, 'defense': 5, 'agility': 10, 'skills': ['Fireball', 'Heal']})
        elif player_class == 'Rogue':
            self.player.update({'strength': 10, 'defense': 10, 'agility': 15, 'skills': ['Backstab', 'Dodge']})
        self.popup.dismiss()
        self.info_label.text = f"Welcome to Flufftopia, {self.player['name']} the {self.player['class']}!"
        grant_dev_privileges(self)
        self.game_intro()

    def game_intro(self):
        intro_text = (
            "Welcome to Flufftopia!\n"
            "In a land of mystery and magic, you will embark on a journey like no other.\n"
            "Explore ancient ruins, enchanted forests, and hidden villages.\n"
            "Uncover secrets long forgotten and treasures untold.\n"
            "Your goal is to survive, grow stronger, and uncover the ultimate treasure.\n"
            "Good luck, brave adventurer!\n"
        )
        self.info_label.text = intro_text

    def player_setup(self):
        player = {
            "name": "Hero",
            "class": "None",
            "health": 100,
            "strength": 10,
            "defense": 5,
            "agility": 5,
            "inventory": ["health potion"],
            "quests": [],
            "xp": 0,
            "level": 1,
            "skills": []
        }
        return player

    def clear_screen(self):
        self.info_label.text = ""

    def describe_location(self, location):
        self.info_label.text += f"\nYou are at the {location.replace('_', ' ').title()}.\n{locations[location]['description']}"

    def random_event(self, location):
        self.clear_screen()
        if location in events:
            event = random.choice(events[location])
            self.info_label.text += f"\n{event}"
            if "guardian" in event or "encounter" in event:
                self.current_enemy = random.choice(enemies)
                self.info_label.text += f"\nA wild {self.current_enemy['name']} appears!"
                self.enable_combat_buttons(True)
                self.display_enemy_stats(self.current_enemy)
            elif "trap" in event or "escape" in event:
                self.player["health"] -= 10
                self.health_bar.value = self.player["health"]
                self.info_label.text += f"\nYou lose 10 health. Current health: {self.player['health']}"
            elif "potion" in event or "healing" in event:
                self.player["health"] = min(100, self.player["health"] + 10)
                self.health_bar.value = self.player["health"]
                self.info_label.text += f"\nYou gain 10 health. Current health: {self.player['health']}"
        self.check_player_health()

    def combat(self, enemy):
        self.clear_screen()
        self.info_label.text += f"\n{self.player['name']}'s Health: {self.player['health']}"
        self.info_label.text += f"\n{enemy['name']}'s Health: {enemy['health']}"

        player_damage = max(0, self.player["strength"] - enemy["defense"] + random.randint(-5, 5))
        enemy["health"] -= player_damage
        self.info_label.text += f"\nYou attack the {enemy['name']} for {player_damage} damage!"

        if enemy["health"] <= 0:
            self.info_label.text += f"\nYou have defeated the {enemy['name']}!"
            loot = random.choice(enemy["loot"])
            self.player["inventory"].append(loot)
            self.inventory_label.text = "Inventory: " + ', '.join(self.player["inventory"])
            self.info_label.text += f"\nYou found a {loot} on the {enemy['name']}!"
            self.enable_combat_buttons(False)
            self.proceed_if_enemy_defeated()
            self.gain_xp(10)
            return

        enemy_damage = max(0, enemy["strength"] - self.player["defense"] + random.randint(-5, 5))
        self.player["health"] -= enemy_damage
        self.health_bar.value = self.player["health"]
        self.info_label.text += f"\nThe {enemy['name']} attacks you for {enemy_damage} damage!"

        self.check_player_health()

    def defend(self, instance):
        self.clear_screen()
        if self.current_enemy:
            self.info_label.text += f"\n{self.player['name']} is defending!"
            self.player["defense"] *= 2
            self.enemy_attack(self.current_enemy)
        else:
            self.info_label.text += "\nNo enemy to defend against."

    def enemy_attack(self, enemy):
        enemy_damage = max(0, enemy["strength"] - self.player["defense"] + random.randint(-5, 5))
        self.player["health"] -= enemy_damage
        self.health_bar.value = self.player["health"]
        self.info_label.text += f"\nThe {enemy['name']} attacks you for {enemy_damage} damage!"
        self.player["defense"] = int(self.player["defense"] / 2)
        self.check_player_health()

    def check_player_health(self):
        if self.player["health"] <= 0:
            self.info_label.text += "\nYou have been defeated. Game over."
            self.next_button.disabled = True
            self.enable_combat_buttons(False)

    def proceed_if_enemy_defeated(self):
        if self.current_enemy and self.current_enemy["health"] <= 0:
            self.current_enemy = None
            self.info_label.text += "\nThe enemy has been defeated."
            self.show_location_choices()

    def next_location(self, instance):
        if self.player["health"] <= 0:
            return

        if self.current_enemy:
            self.info_label.text += f"\nYou must defeat the {self.current_enemy['name']} to proceed!"
            return

        self.show_location_choices()

    def show_location_choices(self):
        if self.location_index < len(locations):
            popup_layout = BoxLayout(orientation='vertical')
            popup_scroll = ScrollView()
            grid_layout = GridLayout(cols=1, size_hint_y=None)
            grid_layout.bind(minimum_height=grid_layout.setter('height'))
            popup_scroll.add_widget(grid_layout)

            for loc in locations.keys():
                if loc in self.unlocked_locations:
                    btn = Button(text=loc.replace('_', ' ').title(), size_hint_y=None, height=40)
                    btn.bind(on_press=lambda instance, loc=loc: self.select_location(loc))
                    grid_layout.add_widget(btn)

            popup_layout.add_widget(popup_scroll)
            self.location_popup = Popup(title="Choose Your Next Location", content=popup_layout, size_hint=(0.75, 0.75))
            self.location_popup.open()

    def select_location(self, location):
        self.clear_screen()
        self.describe_location(location)
        self.random_event(location)
        self.location_popup.dismiss()

    def explore_area(self, instance):  # Added explore area method
        self.clear_screen()
        if self.current_boss:
            self.info_label.text += "\nYou must defeat the boss to explore further!"
            return

        location = self.unlocked_locations[self.location_index]
        self.describe_location(location)
        self.info_label.text += "\nYou explore the area and find something interesting."
        self.random_event(location)

    def use_skill(self, skill, target, popup):
        self.clear_screen()
        if skill == "Slash" or skill == "s":
            damage = self.player["strength"] * 2 - target["defense"]
            target["health"] -= max(0, damage)
            self.info_label.text += f"\nYou use Slash on {target['name']} for {damage} damage!"
        elif skill == "Shield Bash" or skill == "sb":
            damage = self.player["strength"] - target["defense"]
            target["health"] -= max(0, damage)
            self.player["defense"] += 5
            self.info_label.text += f"\nYou use Shield Bash on {target['name']} for {damage} damage!"
        elif skill == "Fireball" or skill == "f":
            damage = self.player["strength"] * 2 - target["defense"]
            target["health"] -= max(0, damage)
            self.info_label.text += f"\nYou cast Fireball at {target['name']} for {damage} damage!"
        elif skill == "Heal" or skill == "h":
            heal_amount = self.player["strength"] * 2
            self.player["health"] = min(100, self.player["health"] + heal_amount)
            self.health_bar.value = self.player["health"]
            self.info_label.text += f"\nYou heal yourself for {heal_amount} health points!"
        elif skill == "Backstab" or skill == "b":
            damage = self.player["strength"] * 3 - target["defense"]
            target["health"] -= max(0, damage)
            self.info_label.text += f"\nYou use Backstab on {target['name']} for {damage} damage!"
        elif skill == "Dodge" or skill == "d":
            self.player["agility"] += 10
            self.info_label.text += f"\nYou use Dodge and increase your agility!"
        popup.dismiss()
        self.check_player_health()
        self.proceed_if_enemy_defeated()

    def show_skill_popup(self, instance):
        layout = BoxLayout(orientation='vertical')
        skill_buttons = []

        for skill in self.player["skills"]:
            btn = Button(text=skill, size_hint=(1, 0.5))
            btn.bind(on_press=lambda x, s=skill: self.use_skill(s, self.current_enemy if s not in ["Heal", "Dodge"] else self.player, popup))
            skill_buttons.append(btn)

        for btn in skill_buttons:
            layout.add_widget(btn)

        popup = Popup(title="Choose a Skill", content=layout, size_hint=(0.5, 0.3))
        popup.open()

    def attack_enemy(self, instance):
        if self.current_enemy:
            self.combat(self.current_enemy)
        else:
            self.info_label.text += "\nNo enemy to attack."

    def run_from_combat(self, instance):
        if self.current_enemy:
            self.info_label.text += f"\nYou must defeat the {self.current_enemy['name']} to proceed!"
        else:
            self.info_label.text += "\nNo enemy to run from."

    def enable_combat_buttons(self, enable):
        self.attack_button.disabled = not enable
        self.defend_button.disabled = not enable
        self.skill_button.disabled = not enable
        self.run_button.disabled = not enable

    def display_enemy_stats(self, enemy):
        self.info_label.text += (
            f"\nEnemy: {enemy['name']}\n"
            f"Health: {enemy['health']}\n"
            f"Strength: {enemy['strength']}\n"
            f"Defense: {enemy['defense']}\n"
        )

    def gain_xp(self, amount):
        self.player["xp"] += amount
        self.info_label.text += f"\nYou gained {amount} XP."
        if self.player["xp"] >= self.player["level"] * 10:
            self.level_up()

    def level_up(self):
        self.player["level"] += 1
        self.player["xp"] = 0
        self.player["strength"] += 5
        self.player["defense"] += 5
        self.player["agility"] += 5
        self.info_label.text += f"\nCongratulations! You leveled up to level {self.player['level']}."
        self.info_label.text += (
            f"\nNew stats:\n"
            f"Strength: {self.player['strength']}\n"
            f"Defense: {self.player['defense']}\n"
            f"Agility: {self.player['agility']}"
        )
        self.unlock_new_skill()

    def unlock_new_skill(self):
        new_skills = {
            "Warrior": ["Power Strike", "Battle Cry"],
            "Mage": ["Lightning Bolt", "Mana Shield"],
            "Rogue": ["Shadow Step", "Poison Blade"]
        }
        available_skills = new_skills[self.player["class"]]
        new_skill = random.choice(available_skills)
        self.player["skills"].append(new_skill)
        self.info_label.text += f"\nYou unlocked a new skill: {new_skill}!"

    def unlock_new_location(self):
        new_locations = {

            "level_2": ["ancient_ruins",],
            "level_3": ["enchanted_forest"],
            "level_4": ["hidden_village"],
        }
        current_level = f"level_{self.player['level']}"
        if current_level in new_locations:
            for loc in new_locations[current_level]:
                if loc not in self.unlocked_locations:
                    self.unlocked_locations.append(loc)
                    self.info_label.text += f"\nYou unlocked a new location: {loc.replace('_', ' ').title()}!"

if __name__ == "__main__":
    FlufftopiaApp().run()
