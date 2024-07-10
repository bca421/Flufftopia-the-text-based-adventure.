# main.py
from enemies import enemies
from events import events
from locations import locations
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


class FlufftopiaApp(App):
    def build(self):
        self.player = self.player_setup()
        self.location_index = 0
        self.current_enemy = None

        self.main_layout = BoxLayout(orientation='vertical')

        self.health_bar = ProgressBar(max=100, value=self.player['health'])
        self.main_layout.add_widget(self.health_bar)

        self.info_label = Label(text="Welcome to Flufftopia!", size_hint_y=None, height=400)
        self.scroll_view = ScrollView(size_hint=(1, None), size=(400, 400))
        self.scroll_view.add_widget(self.info_label)
        self.main_layout.add_widget(self.scroll_view)

        self.inventory_label = Label(text="Inventory: " + ', '.join(self.player['inventory']))
        self.main_layout.add_widget(self.inventory_label)

        button_layout = GridLayout(cols=5, size_hint_y=None, height=50)
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

        self.enable_combat_buttons(False)  # Disable combat buttons initially

        self.name_input_popup()

        return self.main_layout

    def name_input_popup(self):
        layout = BoxLayout(orientation='vertical')
        self.name_input = TextInput(hint_text='Enter your name', size_hint=(1, 0.5), multiline=False)
        submit_button = Button(text='Submit', size_hint=(1, 0.5))
        submit_button.bind(on_press=self.set_player_name)

        layout.add_widget(self.name_input)
        layout.add_widget(submit_button)

        self.popup = Popup(title='Player Name', content=layout, size_hint=(0.5, 0.3), auto_dismiss=False)
        self.popup.open()
        self.name_input.focus = True

    def set_player_name(self, instance):
        self.player['name'] = self.name_input.text.strip()
        self.popup.dismiss()
        self.info_label.text = f"Welcome to Flufftopia, {self.player['name']}!"
        self.grant_dev_privileges()

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
            "health": 100,
            "strength": random.randint(10, 20),
            "defense": random.randint(5, 15),
            "agility": random.randint(5, 15),
            "inventory": ["health potion"],
            "quests": []
        }
        return player

    def grant_dev_privileges(self):
        if self.player['name'].lower() == "brian allen":
            self.info_label.text += "\nDeveloper mode activated. You have full access to all functions."

            dev_button_layout = GridLayout(cols=2, size_hint_y=None, height=100)
            self.main_layout.add_widget(dev_button_layout)

            test_combat_button = Button(text="Test Combat")
            test_combat_button.bind(on_press=self.dev_test_combat)
            dev_button_layout.add_widget(test_combat_button)

            test_random_event_button = Button(text="Test Random Event")
            test_random_event_button.bind(on_press=self.dev_test_random_event)
            dev_button_layout.add_widget(test_random_event_button)

            test_next_location_button = Button(text="Test Next Location")
            test_next_location_button.bind(on_press=self.dev_test_next_location)
            dev_button_layout.add_widget(test_next_location_button)

            test_use_skill_button = Button(text="Test Use Skill")
            test_use_skill_button.bind(on_press=self.dev_test_use_skill)
            dev_button_layout.add_widget(test_use_skill_button)

    def dev_test_combat(self, instance):
        self.clear_screen()
        self.current_enemy = random.choice(enemies)
        self.info_label.text += f"\nTesting combat with {self.current_enemy['name']}."
        self.enable_combat_buttons(True)

    def dev_test_random_event(self, instance):
        self.clear_screen()
        location = random.choice(list(events.keys()))
        self.info_label.text += f"\nTesting random event at {location.replace('_', ' ').title()}."
        self.random_event(location)

    def dev_test_next_location(self, instance):
        self.clear_screen()
        self.info_label.text += "\nTesting next location."
        self.next_location(None)

    def dev_test_use_skill(self, instance):
        self.clear_screen()
        self.info_label.text += "\nTesting use skill."
        self.show_skill_popup(None)

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

        damage = max(0, self.player["strength"] - enemy["defense"] + random.randint(-5, 5))
        enemy["health"] -= damage
        self.info_label.text += f"\nYou attack the {enemy['name']} for {damage} damage!"

        if enemy["health"] <= 0:
            self.info_label.text += f"\nYou have defeated the {enemy['name']}!"
            loot = random.choice(enemy["loot"])
            self.player["inventory"].append(loot)
            self.inventory_label.text = "Inventory: " + ', '.join(self.player["inventory"])
            self.info_label.text += f"\nYou found a {loot} on the {enemy['name']}!"
            self.enable_combat_buttons(False)
            self.proceed_if_enemy_defeated()
            return

        damage = max(0, enemy["strength"] - self.player["defense"] + random.randint(-5, 5))
        self.player["health"] -= damage
        self.health_bar.value = self.player["health"]
        self.info_label.text += f"\nThe {enemy['name']} attacks you for {damage} damage!"

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
        damage = max(0, enemy["strength"] - self.player["defense"] + random.randint(-5, 5))
        self.player["health"] -= damage
        self.health_bar.value = self.player["health"]
        self.info_label.text += f"\nThe {enemy['name']} attacks you for {damage} damage!"
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

    def use_skill(self, skill, target, popup):
        self.clear_screen()
        if skill == "fireball" or skill == "f":
            damage = self.player["strength"] * 2 - target["defense"]
            target["health"] -= max(0, damage)
            self.info_label.text += f"\nYou cast a fireball at {target['name']} for {damage} damage!"
        elif skill == "heal" or skill == "h":
            heal_amount = self.player["strength"] * 2
            self.player["health"] = min(100, self.player["health"] + heal_amount)
            self.health_bar.value = self.player["health"]
            self.info_label.text += f"\nYou heal yourself for {heal_amount} health points!"
        popup.dismiss()
        self.check_player_health()
        self.proceed_if_enemy_defeated()

    def show_skill_popup(self, instance):
        layout = BoxLayout(orientation='vertical')
        fireball_button = Button(text="Fireball", size_hint=(1, 0.5))
        heal_button = Button(text="Heal", size_hint=(1, 0.5))

        popup = Popup(title="Choose a Skill", content=layout, size_hint=(0.5, 0.3))
        fireball_button.bind(on_press=lambda x: self.use_skill("fireball", self.current_enemy, popup))
        heal_button.bind(on_press=lambda x: self.use_skill("heal", self.player, popup))
        layout.add_widget(fireball_button)
        layout.add_widget(heal_button)

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

if __name__ == "__main__":
    FlufftopiaApp().run()
