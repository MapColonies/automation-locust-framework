from config import Selection, config

if config[Selection.DEFAULT].TOKEN is None:
    print("Is None")
else:
    print("TOKEN")
