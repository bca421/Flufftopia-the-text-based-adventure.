from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
import random
from enemies import enemies
from events import events
from locations import locations

def grant_dev_privileges(self):
    if self.player['name'].lower() == "brian allen":
        self.info_label.text += "\nDeveloper mode activated. You have full access to all functions."

        dev_button_layout = GridLayout(cols=2, size_hint_y=None, height=200)
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

        increase_health_button = Button(text="Increase Health")
        increase_health_button.bind(on_press=self.dev_increase_health)
        dev_button_layout.add_widget(increase_health_button)

        add_item_button = Button(text="Add Item")
        add_item_button.bind(on_press=self.dev_add_item)
        dev_button_layout.add_widget(add_item_button)

        unlock_location_button = Button(text="Unlock Location")
        unlock_location_button.bind(on_press=self.dev_unlock_location)
        dev_button_layout.add_widget(unlock_location_button)

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

def dev_increase_health(self, instance):
    self.player['health'] = min(100, self.player['health'] + 20)
    self.health_bar.value = self.player['health']
    self.info_label.text += f"\nIncreased health. Current health: {self.player['health']}"

def dev_add_item(self, instance):
    new_item = "mysterious artifact"
    self.player['inventory'].append(new_item)
    self.inventory_label.text = "Inventory: " + ', '.join(self.player['inventory'])
    self.info_label.text += f"\nAdded {new_item} to inventory."

def dev_unlock_location(self, instance):
    new_location = "secret_cave"
    if new_location not in self.unlocked_locations:
        self.unlocked_locations.append(new_location)
        self.info_label.text += f"\nUnlocked new location: {new_location.replace('_', ' ').title()}!"
