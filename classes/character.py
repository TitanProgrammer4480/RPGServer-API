class Character:
  def __init__(self, id, name, location, race, specialisation, skills, abilities, quests):
    self.id = id
    self.name = name #str
    self.location = location
    self.race = race #str
    self.specialisation = specialisation #str
    self.skills = skills #list(skills)
    self.abilities = abilities #list()
    self.quests = quests #list(int(id))

  def to_dict(self):
    return {"id": self.id, 
            "name": self.name, 
            "location": self.location, 
            "race": self.race, 
            "specialisation": self.specialisation,
            "stats": {
                "skills": self.skills,  
                "abilities": self.abilities, 
                "quests": self.quests
                }
            } 
  
  def __repr__(self):
    pass
