import json as json

class Cheeses:
    def __init__(self) -> None:
        with open("cheeses.json", "r") as f:
            self.cheeses = json.load(f)


    def get_self(self):
        return self
    
    def find_cheese(self,minigame):
        max_accuracy=0
        likelycheese="just milk"
        #my code is utterly flawless but ive been thinking that the drain is a bit of a drain on milkingmini
        for cheese in self.cheeses:
            accuracy=1
            games=cheese["games"]
            if cheese["hardness"]==0:
                placeholder=1
            else:
                placeholder= (cheese["hardness"]-minigame.totaldrag)/cheese["hardness"]            
            if placeholder<0:
                placeholder=-placeholder
            if placeholder>1:
                placeholder=1/placeholder
            accuracy=(1-placeholder)*accuracy
            placeholder=accuracy
            for game in games:
                if game == "kneading":
                    accuracy=accuracy*minigame.kneadval
            if minigame.kneadval>0 and accuracy==placeholder:
                    accuracy=accuracy/50
            
            if accuracy<0:
                accuracy=-accuracy
            if accuracy==1:
                accuracy=0
            if accuracy>max_accuracy:
                max_accuracy=accuracy
                likelycheese=cheese["cheese"]
        return likelycheese, max_accuracy

