class User:
  def __init__(self, username, id, char_ids, char_slots):
    self.id = id
    self.username = username # str
    self.char_ids = char_ids# list(ints)
    self.char_slots = char_slots

  def to_dict(self):
    return {"id": self.id, "user": self.username, "char_ids": self.char_ids, "char_slots": self.char_slots}
  
  def __repr__(self):
    return f"User(id={self.id}, username={self.username})"
