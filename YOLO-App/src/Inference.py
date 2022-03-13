import cv2, os, time, subprocess
import pandas as pd
from autocorrect import Speller

class Inference:
    def __init__(self, darknetPath, configPath, weightPath, dataPath):
        
        self.darknetPath = darknetPath
        self.configPath = configPath
        self.weightPath = weightPath
        self.dataPath = dataPath
        
        self.autoCorrect = Speller()
        
        self.thresholds = {2: 0.25, 
                            3: 0.2, 
                            4: 0.1,
                            5: 0.08,
                            6: 0.07,
                            7: 0.05,
                            8: 0.04,
                            9: 0.03,
                            10: 0.027
                        }

    def _getLineCount(self, imgPath):
        
        try:
            img = cv2.imread(imgPath)
        except:
            print("Invalid path")
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  

        #--- performing Otsu threshold ---
        ret,thresh1 = cv2.threshold(gray, 0, 255,cv2.THRESH_OTSU|cv2.THRESH_BINARY_INV)

        #--- choosing the right kernel
        #--- kernel size of 3 rows (to join dots above letters 'i' and 'j')
        #--- and 10 columns to join neighboring letters in words and neighboring words
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (75, 3))
        dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)

        #---Finding contours ---
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        im2 = img.copy()
        conwidth=list()
        for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                conwidth.append(w)
                cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

        maxwidth=max(conwidth)
        threshwidth=int(1/7 * maxwidth)
        counter=0
        for i in conwidth:
                if i<threshwidth:
                        counter=counter+1

                else:
                        pass
        # print("Counter",counter)
        # print("No of sentences",len(contours)-counter)
        numOfLines=len(contours)-counter
        return numOfLines
    
    def _getThreshold(self, numOfLines):
        
        if numOfLines in self.thresholds:
            return self.thresholds[numOfLines]
        else:
            return self.thresholds[10]
        
    def _deltaFunction(self, threshold, inferenceTextFilePath):
        
        bl=list()
        # print("thresh:",threshold)
        with open(inferenceTextFilePath, 'r') as outputFile:
            for line in outputFile:
                line = line.strip().split()
                bl.append(line)

        for i in range(0,len(bl)):
            cval=float(bl[i][3])
            for j in range(0,len(bl)):
                anval=float(bl[j][3])
                if abs(cval-anval)>=threshold:
                    pass
                else:
                    bl[i][3]=bl[j][3]=round(float(bl[i][3]),2)
                    
        return bl

    def _getOutput(self, tempResults, autoCorrectFlag):

        df = pd.DataFrame.from_records(tempResults)
        sort_group = df.sort_values(by=[3, 2])

        y = sort_group.groupby(3)
        
        # words=""
        # for name, group in y:
            
        #     for row_index, row in group.iterrows():
        #         # print(row)
        #         wor = str(row[0])
        #         if wor=="Space":
        #         # fans=fans+" "
        #             words=words+" "
        #         # print(wor)
        #         # elif wor=="\\n":
        #         #     words=words+'\n'
        #         else:
        #             words += wor
        #     words += "\n"

        # # print(words)
        # return words
        
        doubleCharList = list()
        for name, group in y:
            
            for row_index, row in group.iterrows():
                
                doubleCharList.append([row[0], row[1], row[2], row[3], row[4], row[5]])
                
        # Removing unwanted characters                
        for i in range(0,len(doubleCharList)-1):

            if doubleCharList[i][0]== doubleCharList[i+1][0]!="l" and \
                abs(float(doubleCharList[i][1])-float(doubleCharList[i+1][1]))>15.00 or \
                    doubleCharList[i][0]== doubleCharList[i+1][0] and \
                        abs(float(doubleCharList[i][2])-float(doubleCharList[i+1][2]))==0.00000000:

                if (float(doubleCharList[i][1]) > float(doubleCharList[i+1][1])):
                    doubleCharList[i+1].append("del")

                elif (float(doubleCharList[i][1]) < float(doubleCharList[i+1][1])):
                    doubleCharList[i].append("del") 
              
        # Removing unwanted characters
              
        for i in range(0,len(doubleCharList)-1):

            if doubleCharList[i][0]!= doubleCharList[i+1][0] and \
                abs(float(doubleCharList[i][2])-float(doubleCharList[i+1][2]))<=0.0005000:

                if(float(doubleCharList[i][1]) > float(doubleCharList[i+1][1])):
                    doubleCharList[i+1].append("del")

                if(float(doubleCharList[i][1]) < float(doubleCharList[i+1][1])):
                    doubleCharList[i].append("del") 
        
        tempDoubleList = list()
                    
        for i in doubleCharList:
            if len(i)!=6:
                pass
            else:
                tempDoubleList.append(i)    
                
        # Added code for swapping         
        for i in range(0,len(tempDoubleList)-1):
            if str(tempDoubleList[i][0]) != str(tempDoubleList[i+1][0]) and \
                str(tempDoubleList[i][2]) == str(tempDoubleList[i+1][2]) and \
                    float(tempDoubleList[i][1]) < float(tempDoubleList[i+1][1]):
                
                tempDoubleList[i],tempDoubleList[i+1]= tempDoubleList[i+1],tempDoubleList[i]
                    
        df = pd.DataFrame.from_records(tempDoubleList)
        sort_group = df.sort_values(by=[3, 2])

        y = sort_group.groupby(3)
        
        output_text = ""
        
        for name, group in y:
            
            for row_index, row in group.iterrows():

                wor = str(row[0])
                if wor=="Space":
                    
                    output_text = output_text + " "
                    
                else:
                    output_text += wor
                    
            output_text += "\n"
            
        if autoCorrectFlag:
            
            return self.autoCorrect(output_text)
        
        return output_text
                    
    def getInferences(self, imagePath, autoCorrectFlag):
        prevDir = os.getcwd()
        os.chdir(self.darknetPath)
        
        # subprocess.Popen(["python3", "darknet_images.py", \
        #     "--input", "{}".format(imagePath), \
        #         "--weights", "{}".format(self.weightPath), \
        #             "--config_file", "{}".format(self.configPath), \
        #                 "--data_file", "{}".format(self.dataPath), \
        #                     "--dont_show","--thresh", "0.3"])
        
        os.system("python3 darknet_images.py --input {} --weights {} --config_file {} --data_file {} --dont_show"
                  .format(imagePath, self.weightPath, self.configPath, self.dataPath))
        
        numLines = self._getLineCount(imagePath)
        threshold = self._getThreshold(numLines)
        
        inferenceTextFilePath = imagePath.split(".")[0] + ".txt"
        
        while not os.path.exists(inferenceTextFilePath):
            time.sleep(1)
        
        tempResults = self._deltaFunction(threshold, inferenceTextFilePath)
        
        output_text = self._getOutput(tempResults, autoCorrectFlag)
        
        os.chdir(prevDir)
        
        return output_text