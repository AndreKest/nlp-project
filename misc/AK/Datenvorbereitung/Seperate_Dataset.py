# Seperate the dataset
import json
import gzip
import shutil
import os

counter = 1

with gzip.open(os.path.join("top1000.json" + ".gz"), 'w') as f_out:
    with open("2019-02-19_oldp_cases.json", "r") as f_in:
        for line in f_in:
            text = json.loads(line)
            f_out.write((json.dumps(text) + '\n').encode('utf-8'))
            if counter == 1000:
                break

            # write dataset line by line
            # open stream
            # output = open("./Dataset_RAW_Content/CourtDecision_"+str(counter)+".json", 'w')
            # json.dump(text, output)
            # output.write(text['content'])
            # output.close()

            counter += 1

print(text['content'])

print("Process finished!")