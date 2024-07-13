# dev_privileges.py

from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
import random
from enemies import enemies
from events import events
from locations import locations

def grant_dev_privileges(self):
    if self.player['name'].lower() == "brian allen":
        self.info_label.text += "\nAdmin mode activated. You have access to some functions."

        self.player["health"] += 99999900 # Increase health for admin user
        self.player["strength"] += 500
        self.player["defense"] += 500
        self.player["agility"] += 500
        '''self.player['name'].lower() == "brian allen":
        self.info_label.text += "\nDeveloper mode activated. You have full access to all functions."

        dev_button_layout = GridLayout(cols=2, size_hint_y=None, height=200)
        self.main_layout.add_widget(dev_button_layout)

        buttons = [
            ("Test Combat", self.dev_test_combat),
            ("Test Random Event", self.dev_test_random_event),
            ("Test Next Location", self.dev_test_next_location),
            ("Test Use Skill", self.dev_test_use_skill),
            ("Increase Health", self.dev_increase_health),
            ("Add Item", self.dev_add_item),
            #("Unlock Location", self.dev_unlock_location)
        ]

        for text, func in buttons:
            btn = Button(text=text)
            btn.bind(on_press=func)
            dev_button_layout.add_widget(btn)'''
    elif self.player['name'].lower() == "erin allen":
        self.info_label.text += "\nAdmin mode activated. You have access to some functions."

        self.player["health"] += 99999900 # Increase health for admin user
        self.player["strength"] += 500
        self.player["defense"] += 500
        self.player["agility"] += 500
        
        
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
