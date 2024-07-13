from enemies import enemies
from events import events
from dev_privileges import grant_dev_privileges
from locations import locations
from bosses import bosses
import random
import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout


def grant_dev_privileges(self):
    if self.player['name'].lower() == "brian allen":
        self.info_label.text += "\nAdmin mode activated. You have access to some functions."

        self.player["health"] += 99999900 # Increase health for admin user
        self.player["strength"] += 500
        self.player["defense"] += 500
        self.player["agility"] += 500

    elif self.player['name'].lower() == "erin allen":
        self.info_label.text += "\nAdmin mode activated. You have access to some functions."

        self.player["health"] += 99999900 # Increase health for admin user
        self.player["strength"] += 500
        self.player["defense"] += 500
        self.player["agility"] += 500

class FlufftopiaApp(App):
    def build(self):
        self.player = None
        self.current_location = "village"  # Initial location
        self.current_enemy = None
        self.current_boss = None
        self.unlocked_locations = ["village", "enchanted_forest", "ancient_ruins"]

        self.main_layout = BoxLayout(orientation='vertical')

        self.create_player_screen()

        return self.main_layout

    def create_player_screen(self):
        self.main_layout.clear_widgets()

        self.info_label = Label(text="Welcome to Flufftopia! Please enter your details below.", size_hint_y=None, height=200)
        self.main_layout.add_widget(self.info_label)

        self.name_input = TextInput(hint_text="Enter your name", multiline=False, size_hint_y=None, height=50)
        self.main_layout.add_widget(self.name_input)

        self.class_label = Label(text="Choose your class", size_hint_y=None, height=50)
        self.main_layout.add_widget(self.class_label)

        class_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        self.main_layout.add_widget(class_layout)

        self.class_choice = None

        classes = ["Warrior", "Mage", "Rogue"]
        for c in classes:
            btn = Button(text=c, size_hint_y=None, height=50)
            btn.bind(on_press=lambda instance, c=c: self.set_class(c))
            class_layout.add_widget(btn)

        self.submit_button = Button(text="Create Player", size_hint_y=None, height=50)
        self.submit_button.bind(on_press=self.create_player)
        self.main_layout.add_widget(self.submit_button)

    def set_class(self, chosen_class):
        self.class_choice = chosen_class
        self.class_label.text = f"Chosen class: {chosen_class}"

    def create_player(self, instance):
        player_name = self.name_input.text.strip()

        if not player_name or not self.class_choice:
            self.show_popup("Error", "Both name and class must be provided.")
            return

        initial_skills = {
            "Warrior": ["Slash", "Shield Bash"],
            "Mage": ["Fireball", "Ice Shard"],
            "Rogue": ["Backstab", "Poison Dart"]
        }

        self.player = {
            "name": player_name,
            "class": self.class_choice,
            "health": 100,
            "strength": 10,
            "defense": 5,
            "agility": 5,
            "inventory": ["health potion"],
            "quests": [],
            "xp": 0,
            "level": 1,
            "skills": initial_skills[self.class_choice]
        }

        with open("player_data.json", "w") as f:
            json.dump(self.player, f)

        self.show_popup("Success", f"Player {player_name} the {self.class_choice} created successfully!")

        grant_dev_privileges(self)  # Grant developer privileges if applicable
        
        self.start_game()

    def start_game(self):
        self.main_layout.clear_widgets()
        self.build_game_ui()

    # ... (rest of your code)


    def build_game_ui(self):
        self.health_bar = ProgressBar(max=100, value=self.player['health'])
        self.main_layout.add_widget(self.health_bar)

        self.info_label = Label(text=f"Welcome to Flufftopia, {self.player['name']}!", size_hint_y=None, height=200)
        self.scroll_view = ScrollView(size_hint=(1, None), size=(400, 400))
        self.scroll_view.add_widget(self.info_label)
        self.main_layout.add_widget(self.scroll_view)

        self.inventory_label = Label(text="Inventory: " + ', '.join(self.player['inventory']))
        self.main_layout.add_widget(self.inventory_label)

        self.skills_label = Label(text="Skills: " + ', '.join(self.player['skills']))
        self.main_layout.add_widget(self.skills_label)

        button_layout = GridLayout(cols=6, size_hint_y=None, height=50)
        self.main_layout.add_widget(button_layout)

        self.next_button = Button(text="Location")
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

        self.inventory_button = Button(text="Inventory")
        self.inventory_button.bind(on_press=self.show_inventory_popup)
        button_layout.add_widget(self.inventory_button)

        self.enable_combat_buttons(False)  # Disable combat buttons initially

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical')
        popup_label = Label(text=message)
        close_button = Button(text="Close", size_hint_y=None, height=50)
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(close_button)

        popup = Popup(title=title, content=popup_layout, size_hint=(0.5, 0.5))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

    # Remaining methods from your original code (combat, exploration, skill usage, etc.)

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
                self.enable_exploration_buttons(False)
                self.enable_next_buttons(False)
            elif "boss" in event or "huge" in event:
                self.current_enemy = random.choice(bosses)
                self.info_label.text += f"\nA wild {self.current_enemy['name']} appears!"
                self.enable_combat_buttons(True)
                self.enable_exploration_buttons(False)
                self.enable_next_buttons(False)
            elif "trap" in event or "escape" in event:
                self.player["health"] -= 10
                self.health_bar.value = self.player["health"]
                self.info_label.text += f"\nYou lose 10 health. Current health: {self.player['health']}"
            elif "potion" in event or "healing" in event:
                self.player["health"] = min(100, self.player["health"] + 10)
                self.health_bar.value = self.player["health"]
                self.info_label.text += f"\nYou gain 10 health. Current health: {self.player['health']}"
            elif "shop" in event:
                self.open_shop()
        self.check_player_health()

    def combat(self, enemy):
        self.clear_screen()
        self.info_label.text += f"\n{self.player['name']}'s Health: {self.player['health']}"
        self.info_label.text += f"\n{enemy['name']}'s Health: {enemy['health']}"

        player_damage = max(0, self.player["strength"] - enemy["defense"] + random.randint(-5, 5))
        enemy["health"] -= player_damage
        self.info_label.text += f"\nYou attack the {enemy['name']} for {player_damage} damage!"

        if enemy["health"] <= 0:
            self.proceed_if_enemy_defeated()
            return

        enemy_damage = max(0, enemy["strength"] - self.player["defense"] + random.randint(-5, 5))
        self.player["health"] -= enemy_damage
        self.health_bar.value = self.player["health"]
        self.info_label.text += f"\nThe {enemy['name']} attacks you for {enemy_damage} damage!"
        self.enable_exploration_buttons(False)
        self.enable_next_buttons(False)

        self.check_player_health()

    def defend(self, instance):
        self.clear_screen()
        if self.current_enemy:
            self.display_player_stats()
            self.display_enemy_stats(self.current_enemy)
            self.info_label.text += f"\n{self.player['name']} is defending!"
            reduced_damage = max(0, self.current_enemy["strength"] - (self.player["defense"] * 2) + random.randint(-5, 5))
            self.player["health"] -= reduced_damage
            self.health_bar.value = self.player["health"]
            self.info_label.text += f"\nThe {self.current_enemy['name']} attacks you for {reduced_damage} reduced damage!"
            self.check_player_health()

    def check_player_health(self):
        if self.player["health"] <= 0:
            self.info_label.text += f"\n{self.player['name']} has been defeated. Game over."
            self.enable_combat_buttons(False)
            self.enable_exploration_buttons(False)
            self.enable_next_buttons(False)

    def gain_xp(self, amount):
        self.player["xp"] += amount
        self.info_label.text += f"\nYou gained {amount} XP. Total XP: {self.player['xp']}"
        self.level_up()

    def level_up(self):
        level_thresholds = [100 * (i + 1) for i in range(20)]  # XP thresholds for levels 1 to 20
        current_level = self.player["level"]

        if current_level <= 20 and self.player["xp"] >= level_thresholds[current_level - 1]:
            self.player["level"] += 1
            self.player["xp"] -= level_thresholds[current_level - 1]
            self.player["health"] = 100 + (self.player["level"] - 1) * 10  # Adjusted to avoid overly high health
            self.player["strength"] += 5
            self.player["defense"] += 5
            self.player["agility"] += 5
            self.info_label.text += f"\nCongratulations! You have reached level {self.player['level']}!"
            self.display_player_stats()
            self.health_bar.value = self.player["health"]
            self.unlock_new_skill()
            self.unlock_new_location()

    def display_player_stats(self):
        self.info_label.text += f"\nPlayer Stats: Level {self.player['level']}, Health {self.player['health']}, Strength {self.player['strength']}, Defense {self.player['defense']}, Agility {self.player['agility']}"

    def display_enemy_stats(self, enemy):
        if enemy:  # Ensure enemy is not None
            self.info_label.text += f"\nEnemy Stats: {enemy['name']}, Health {enemy['health']}, Strength {enemy['strength']}, Defense {enemy['defense']}"

    def enable_exploration_buttons(self, enable):
        self.explore_button.disabled = not enable

    def enable_next_buttons(self, enable):
        self.next_button.disabled = not enable

    def enable_combat_buttons(self, enable):
        self.attack_button.disabled = not enable
        self.defend_button.disabled = not enable
        self.run_button.disabled = not enable
        self.skill_button.disabled = not enable

    def attack_enemy(self, instance):
        if self.current_enemy:
            self.combat(self.current_enemy)

    def run_from_combat(self, instance):
        self.clear_screen()
        if self.current_enemy:
            if random.random() < 0.5:
                self.info_label.text += f"\nYou successfully ran away from the {self.current_enemy['name']}!"
                self.current_enemy = None
                self.enable_combat_buttons(False)
                self.enable_exploration_buttons(True)
                self.enable_next_buttons(True)
            else:
                self.info_label.text += f"\nFailed to run away from the {self.current_enemy['name']}!"
                self.combat(self.current_enemy)
                self.display_player_stats()
                self.display_enemy_stats(self.current_enemy)

    def explore_area(self, instance):
        self.clear_screen()
        self.describe_location(self.current_location)
        if random.random() < 0.5:
            self.random_event(self.current_location)
        else:
            self.info_label.text += "\nNothing of interest found while exploring."

    def next_location(self, instance):
        self.clear_screen()
        popup_layout = BoxLayout(orientation='vertical')
        popup_layout.add_widget(Label(text="Choose your next location:"))

        for loc in self.unlocked_locations:
            btn = Button(text=loc.replace("_", " ").title())
            btn.bind(on_press=lambda btn: self.set_location(btn.text.lower().replace(" ", "_")))
            popup_layout.add_widget(btn)

        close_button = Button(text="Close")
        close_button.bind(on_press=lambda btn: self.popup.dismiss())
        popup_layout.add_widget(close_button)

        self.popup = Popup(title="Locations", content=popup_layout, size_hint=(0.9, 0.9))
        self.popup.open()

    def set_location(self, location):
        self.current_location = location
        self.info_label.text += f"\nMoved to {location.replace('_', ' ').title()}."
        self.describe_location(location)
        self.popup.dismiss()

    def show_skill_popup(self, instance):
        self.clear_screen()
        if self.player["skills"]:
            skill_popup_layout = BoxLayout(orientation='vertical')
            skill_popup_layout.add_widget(Label(text="Choose a skill to use:"))

            for skill in self.player["skills"]:
                btn = Button(text=skill)
                btn.bind(on_press=lambda btn, skill=skill: self.use_skill(skill))
                skill_popup_layout.add_widget(btn)

            close_button = Button(text="Close")
            close_button.bind(on_press=lambda btn: self.skill_popup.dismiss())
            skill_popup_layout.add_widget(close_button)

            self.skill_popup = Popup(title="Skills", content=skill_popup_layout, size_hint=(0.9, 0.9))
            self.skill_popup.open()
        else:
            self.info_label.text += "\nYou have no skills to use."

    def use_skill(self, skill):
        self.clear_screen()
        self.info_label.text += f"\nYou used the skill: {skill}!"

        skill_actions = {
            "Power Strike": self.power_strike,
            "Fireball": self.fireball,
            "Poison Dart": self.poison_dart,
            "Ice Shard": self.ice_shard,
            "Shield Bash": self.shield_bash,
            "Battle Cry": self.battle_cry,
            "Slash": self.slash,
            "Backstab": self.backstab,
            "Lightning Bolt": self.lightning_bolt,
            "Mana Shield": self.mana_shield,
            "Shadow Step": self.shadow_step,
            "Poison Blade": self.poison_blade
        }

        if skill in skill_actions:
            skill_actions[skill]()
        
        self.skill_popup.dismiss()

    def shield_bash(self):
        self.use_combat_skill("Shield Bash", multiplier=1.5)

    def slash(self):
        self.use_combat_skill("Slash", multiplier=1.5)

    def poison_dart(self):
        self.use_combat_skill("Poison Dart", additional_effect="poisoned")

    def ice_shard(self):
        self.use_combat_skill("Ice Shard", multiplier=2, additional_effect="frozen")

    def backstab(self):
        self.use_combat_skill("Backstab", additional_damage=5, additional_effect="poisoned")

    def power_strike(self):
        self.use_combat_skill("Power Strike", multiplier=2)

    def battle_cry(self):
        self.player["strength"] += 5
        self.info_label.text += "\nBattle Cry increases your strength by 5!"

    def lightning_bolt(self):
        self.use_combat_skill("Lightning Bolt", multiplier=3)

    def mana_shield(self):
        self.player["defense"] += 10
        self.info_label.text += "\nMana Shield increases your defense by 10!"

    def shadow_step(self):
        self.player["agility"] += 5
        self.info_label.text += "\nShadow Step increases your agility by 5!"

    def fireball(self):
        self.use_combat_skill("Fireball", additional_damage=10, additional_effect="burned")
    
    def poison_blade(self):
        self.use_combat_skill("Poison Blade", additional_damage=10, additional_effect="poisoned")

    def use_combat_skill(self, skill_name, multiplier=1, additional_damage=0, additional_effect=None):
        if self.current_enemy:
            damage = self.player["strength"] * multiplier + additional_damage
            self.current_enemy["health"] -= damage
            self.info_label.text += f"\n{skill_name} deals {damage} damage to {self.current_enemy['name']}!"
            if additional_effect:
                self.current_enemy[additional_effect] = True
                self.info_label.text += f"\n{self.current_enemy['name']} is now {additional_effect}!"
            self.proceed_if_enemy_defeated()

    def proceed_if_enemy_defeated(self):
        if self.current_enemy and self.current_enemy["health"] <= 0:
            self.info_label.text += f"\nYou have defeated the {self.current_enemy['name']}!"
            loot = random.choice(self.current_enemy["loot"])
            self.player["inventory"].append(loot)
            self.inventory_label.text = "Inventory: " + ', '.join(self.player["inventory"])
            self.info_label.text += f"\nYou found a {loot} on the {self.current_enemy['name']}!"
            self.enable_combat_buttons(False)
            self.enable_exploration_buttons(True)
            self.enable_next_buttons(True)            
            self.gain_xp(10)
            self.current_enemy = None

    def open_shop(self):
        self.clear_screen()
        self.info_label.text += "\nYou have encountered a shop!"
        # Generate shop items
        self.shop_items = self.generate_shop_items()
        if not self.shop_items:
            self.info_label.text += "\nNo items available in the shop."
            return
        # Show shop popup
        self.show_shop_popup()

    def generate_shop_items(self):
        items = [
            {"name": "Health Potion", "price": 50},
            {"name": "Mana Potion", "price": 50},
            {"name": "Strength Elixir", "price": 100},
            {"name": "Defense Amulet", "price": 100},
            {"name": "Agility Boots", "price": 100},
        ]
        # Randomly select items
        selected_items = random.sample(items, k=random.randint(2, 5))
        return selected_items

    def show_shop_popup(self):
        shop_popup_layout = BoxLayout(orientation='vertical')
        shop_popup_layout.add_widget(Label(text="Welcome to the shop!"))

        for item in self.shop_items:
            btn = Button(text=f"{item['name']} - {item['price']} gold")
            btn.bind(on_press=lambda btn, item=item: self.purchase_item(item))
            shop_popup_layout.add_widget(btn)

        close_button = Button(text="Close")
        close_button.bind(on_press=lambda btn: self.shop_popup.dismiss())
        shop_popup_layout.add_widget(close_button)

        self.shop_popup = Popup(title="Shop", content=shop_popup_layout, size_hint=(0.9, 0.9))
        self.shop_popup.open()

    def purchase_item(self, item):
        if "gold" not in self.player:
            self.player["gold"] = 1000  # Example starting amount

        if self.player["gold"] >= item["price"]:
            self.player["gold"] -= item["price"]
            self.player["inventory"].append(item["name"])
            self.inventory_label.text = "Inventory: " + ', '.join(self.player["inventory"])
            self.info_label.text += f"\nYou purchased a {item['name']}!"
        else:
            self.info_label.text += "\nYou don't have enough gold!"

    def show_inventory_popup(self, instance):
        inventory_popup_layout = BoxLayout(orientation='vertical')
        inventory_popup_layout.add_widget(Label(text="Your Inventory:"))

        for item in self.player["inventory"]:
            btn = Button(text=item)
            btn.bind(on_press=lambda btn, item=item: self.use_inventory_item(item))
            inventory_popup_layout.add_widget(btn)

        close_button = Button(text="Close")
        close_button.bind(on_press=lambda btn: self.inventory_popup.dismiss())
        inventory_popup_layout.add_widget(close_button)

        self.inventory_popup = Popup(title="Inventory", content=inventory_popup_layout, size_hint=(0.9, 0.9))
        self.inventory_popup.open()

    def use_inventory_item(self, item):
        if item == "health potion":
            self.player["health"] = min(100, self.player["health"] + 20)
            self.health_bar.value = self.player["health"]
            self.player["inventory"].remove(item)
            self.inventory_label.text = "Inventory: " + ', '.join(self.player["inventory"])
            self.info_label.text += f"\nYou used a {item}. Health is now {self.player['health']}."
        self.inventory_popup.dismiss()

        # If in combat, re-enable combat buttons and update enemy stats
        if self.current_enemy:
            self.display_enemy_stats(self.current_enemy)
            self.enable_combat_buttons(True)

    # Developer functions
    def dev_test_combat(self, instance):
        self.clear_screen()
        self.current_enemy = random.choice(enemies)
        self.info_label.text += f"\nTesting combat with {self.current_enemy['name']}."
        self.enable_combat_buttons(True)
        self.display_enemy_stats(self.current_enemy)

    def dev_test_random_event(self, instance):
        self.clear_screen()
        self.random_event(self.current_location)

    def dev_test_next_location(self, instance):
        self.clear_screen()
        self.next_location(instance)

    def dev_test_use_skill(self, instance):
        self.clear_screen()
        self.show_skill_popup(instance)

    def dev_increase_health(self, instance):
        self.clear_screen()
        self.player["health"] = min(100, self.player["health"] + 10)
        self.health_bar.value = self.player["health"]
        self.info_label.text += f"\nHealth increased by 10. Current health: {self.player['health']}"

    def dev_add_item(self, instance):
        self.clear_screen()
        new_item = "magic stone"
        self.player["inventory"].append(new_item)
        self.inventory_label.text = "Inventory: " + ', '.join(self.player["inventory"])
        self.info_label.text += f"\nAdded {new_item} to inventory."

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
            "level_2": ["fairy_glade"],
            "level_3": ["forgotten_tomb"],
            "level_4": ["mystic_mountains"],
            "level_5": ["dragon_lair"],
            "level_6": ["haunted_castle"],
            "level_7": ["hidden_dungeon"],
            "level_8": ["serene_lake"],
            "level_9": ["mystic_island"],
            "level_10": ["desert_oasis"],
            "level_11": ["hidden_sanctuary"],
            "level_12": ["frost_caverns"],
            "level_13": ["ice_palace"],
            "level_14": ["sunken_temple"],
            "level_15": ["treasure_vault", "secret_oasis"],
            "level_16": ["verdant_meadow", "whispering_woods"],
            "level_17": ["underground_grotto", "ancient_tree"],
            "level_18": ["stormy_cliffs", "crystal_caves"],
            "level_19": ["pirate_cove", "crystal_chamber"],
            "level_20": ["burning_desert", "emerald_grove", "healing_spring", "dragon_peak", "dragon_nest"]
        }
        current_level = f"level_{self.player['level']}"
        if current_level in new_locations:
            for loc in new_locations[current_level]:
                if loc not in self.unlocked_locations:
                    self.unlocked_locations.append(loc)
                    self.info_label.text += f"\nYou unlocked a new location: {loc.replace('_', ' ').title()}!"

if __name__ == "__main__":
    FlufftopiaApp().run()
