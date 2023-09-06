# Seperate the dataset
import json

num_text = 50
counter = 1

with open("2019-02-19_oldp_cases.json") as f:
    for line in f:
        court_decision = json.loads(line)

        if counter == num_text:
            break

        counter += 1


# Analyze court decision
print("Keys: ", court_decision.keys())
print("ID: ", court_decision['id'])
print("Slug: ", court_decision['slug'])
print("Court: ", court_decision['court'])
print("file_number: ", court_decision['file_number'])
print("Date: ", court_decision['date'])
print("Created Date: ", court_decision['created_date'])
print("Updated Date: ", court_decision['updated_date'])
print("Type: ", court_decision['type'])
print("Ecli: ", court_decision['ecli'])
print("Content:\n", court_decision['content'])