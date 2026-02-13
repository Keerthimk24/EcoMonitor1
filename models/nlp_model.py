import pickle
import os

# Simple rule-based or trained classifier
# Since we don't have a labeled text dataset provided in the prompt, 
# implementing a keyword-based classifier that simulates "AI" logic 
# or can be easily swapped for a trained sklearn model.

class NLPClassifier:
    def __init__(self):
        self.categories = {
            "Air Pollution": ["smoke", "dust", "fumes", "smog", "air", "breath", "cough", "haze"],
            "Water Pollution": ["water", "river", "lake", "drain", "sewage", "oil", "leak", "dirty water"],
            "Waste Pollution": ["garbage", "trash", "waste", "dump", "plastic", "litter", "rubbish"]
        }

    def predict(self, text):
        text = text.lower()
        scores = {cat: 0 for cat in self.categories}
        
        for cat, keywords in self.categories.items():
            for word in keywords:
                if word in text:
                    scores[cat] += 1
        
        # Return category with max score, default to Air Pollution if unsure
        best_cat = max(scores, key=scores.get)
        if scores[best_cat] == 0:
            return "General Environmental Issue"
        return best_cat

# For structure consistency, we can save this "model" or just import the class.
# We will simulate saving a dummy file so the app feels complete.

def save_dummy_nlp_model():
    model = NLPClassifier()
    # No real training needed for keyword match, but saving for consistency
    pass # No file needed strictly, but app.py will import this script.

def predict_report(text):
    classifier = NLPClassifier()
    return classifier.predict(text)

if __name__ == "__main__":
    # Test
    print(predict_report("There is a lot of garbage in the street."))
