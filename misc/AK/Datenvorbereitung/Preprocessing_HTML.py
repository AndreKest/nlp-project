from bs4 import BeautifulSoup

# max_data = 104763
max_data = 10
num_data = 1

while True:
    # read raw data
    f = open("Dataset_RAW_Content/CourtDecision_"+str(num_data)+".txt", 'r')
    court_decision_raw = f.read()
    soup = BeautifulSoup(court_decision_raw, 'lxml')

    for i in soup.find_all('span'):
        i.append(" ")

    court_decision = soup.get_text()

    # write preprocessed data
    output = open("Test/CourtDecision_"+str(num_data)+".txt", 'w')
    output.write(court_decision)
    output.close()

    if num_data == max_data:
        break

    num_data += 1

f.close()

print("Preprocessing finished!")