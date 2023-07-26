from requirement import *
import csv
# generates list of the requirements met by an agreement for all CCs
def GetListofMetReqs(UniName):
    df = pd.read_csv("csvs/UniSheets/"+UniName+"Gradreqs.csv", header=None, sep='\t')
    row, column = df.shape
    # print(row, column)
    # print(df.iloc[0,1])
    # print(df.iloc[0,2])
    dictreqs = {}
    for i in range(row):
        ccName = df.iloc[i,0]
        courseName = df.iloc[i,1]
        logical_exp = convert_to_logical_expression(convert_to_numerical(ast.literal_eval(courseName)))
        # print(logical_exp)
        articulationName = df.iloc[i,2]
        booleanlists = []
        for item in (ast.literal_eval(articulationName)):
            exp = convert_to_logical_expression(convert_to_boolean(item))
            # print(eval(exp))
            booleanlists.append(eval(exp))
        finalans = substitute_with_bool(logical_exp, booleanlists)
        # print(eval(finalans))

        if(ccName is np.nan):
            continue
        else:
            if(ccName not in list(dict.keys())):
                dict[ccName]= 0
                if eval(finalans) == True:
                    
                    # print(ccName, "requirement met", " in line ", 2*i+1 )
                    dict[ccName]+= 1
                firstone = True
            else:
                if eval(finalans) == True:
                   
                    # print(ccName, "requirement met", " in line ", 2*i-1 )
                    dict[ccName]+= 1

