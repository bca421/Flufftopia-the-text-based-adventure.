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

        if skill == "Power Strike":
            self.power_strike()
        elif skill == "Battle Cry":
            self.battle_cry()
        elif skill == "Slash":
            self.Slash()
        elif skill == "Lightning Bolt":
            self.lightning_bolt()
        elif skill == "Mana Shield":
            self.mana_shield()
        elif skill == "Shadow Step":
            self.shadow_step()
        elif skill == "Poison Blade":
            self.poison_blade()
        
        self.skill_popup.dismiss()

def Slash(self):
        if self.current_enemy:
            damage = self.player["strength"] * 1.5
            self.current_enemy["health"] -= damage
            self.info_label.text += f"\nSlash deals {damage} damage to {self.current_enemy['name']}!"
            self.proceed_if_enemy_defeated()

def power_strike(self):
        if self.current_enemy:
            damage = self.player["strength"] * 2
            self.current_enemy["health"] -= damage
            self.info_label.text += f"\nPower Strike deals {damage} damage to {self.current_enemy['name']}!"
            self.proceed_if_enemy_defeated()

def battle_cry(self):
        self.player["strength"] += 5
        self.info_label.text += "\nBattle Cry increases your strength by 5!"

def lightning_bolt(self):
        if self.current_enemy:
            damage = self.player["strength"] * 3
            self.current_enemy["health"] -= damage
            self.info_label.text += f"\nLightning Bolt deals {damage} damage to {self.current_enemy['name']}!"
            self.proceed_if_enemy_defeated()

def mana_shield(self):
        self.player["defense"] += 10
        self.info_label.text += "\nMana Shield increases your defense by 10!"

def shadow_step(self):
        self.player["agility"] += 5
        self.info_label.text += "\nShadow Step increases your agility by 5!"

def poison_blade(self):
        if self.current_enemy:
            damage = self.player["strength"] + 10
            self.current_enemy["health"] -= damage
            self.info_label.text += f"\nPoison Blade deals {damage} damage to {self.current_enemy['name']} and poisons them!"
            self.current_enemy["poisoned"] = True
            self.proceed_if_enemy_defeated()