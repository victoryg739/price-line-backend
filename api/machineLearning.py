import joblib

def runMl(data):
  # Load the saved model from disk
  treeReg = joblib.load('api/train_model.joblib')
  #Inputs 
  #floorAreaInput  = 'floor_area_sqm_100 - 109SQM'
  floorAreaInput = "floor_area_sqm_" + data["floorArea"]
  remainingLeaseInput = "remaining_lease_" + data["remainingLease"]
  flatModelInput = 'flat_model_' + data["flatModel"]
  townInput = 'town_' + data["town"]
  storeyRangeInput = 'storey_range_' + data["floor"]
  flatTypeInput = 'flat_type_' + data["flatType"]

  # # Create List of Inputs (reference)
  listInput = list((floorAreaInput,remainingLeaseInput,flatModelInput,townInput,storeyRangeInput,flatTypeInput))

  # #List of Columns (Dynamically created)
  colList = ['floor_area_sqm_< 40SQM', 'floor_area_sqm_100 - 109 SQM', 'floor_area_sqm_110 - 119 SQM', 'floor_area_sqm_120 - 129 SQM', 'floor_area_sqm_130 - 139 SQM', 'floor_area_sqm_140 - 149 SQM', 'floor_area_sqm_150 - 159 SQM', 'floor_area_sqm_160 - 169 SQM', 'floor_area_sqm_40 - 49 SQM', 'floor_area_sqm_50 - 59 SQM', 'floor_area_sqm_60 - 69 SQM', 'floor_area_sqm_70 - 79 SQM', 'floor_area_sqm_80 - 89 SQM', 'floor_area_sqm_90 - 99 SQM', 'floor_area_sqm_> 169 SQM', 'remaining_lease_50 - 59 YEARS', 'remaining_lease_60 - 69 YEARS', 'remaining_lease_70 - 79 YEARS', 'remaining_lease_80 - 89 YEARS', 'remaining_lease_< YEARS', 'remaining_lease_> 89 YEARS', 'flat_model_2-room', 'flat_model_3Gen', 'flat_model_Adjoined flat', 'flat_model_Apartment', 'flat_model_DBSS', 'flat_model_Improved', 'flat_model_Improved-Maisonette', 'flat_model_Maisonette', 'flat_model_Model A', 'flat_model_Model A-Maisonette', 'flat_model_Model A2', 'flat_model_Multi Generation', 'flat_model_New Generation', 'flat_model_Premium Apartment', 'flat_model_Premium Apartment Loft', 'flat_model_Premium Maisonette', 'flat_model_Simplified', 'flat_model_Standard', 'flat_model_Terrace', 'flat_model_Type S1', 'flat_model_Type S2', 'town_ANG MO KIO', 'town_BEDOK', 'town_BISHAN', 'town_BUKIT BATOK', 'town_BUKIT MERAH', 'town_BUKIT PANJANG', 'town_BUKIT TIMAH', 'town_CENTRAL AREA', 'town_CHOA CHU KANG', 'town_CLEMENTI', 'town_GEYLANG', 'town_HOUGANG', 'town_JURONG EAST', 'town_JURONG WEST', 'town_KALLANG/WHAMPOA', 'town_MARINE PARADE', 'town_PASIR RIS', 'town_PUNGGOL', 'town_QUEENSTOWN', 'town_SEMBAWANG', 'town_SENGKANG', 'town_SERANGOON', 'town_TAMPINES', 'town_TOA PAYOH', 'town_WOODLANDS', 'town_YISHUN', 'storey_range_11th - 20th', 'storey_range_1st - 10th', 'storey_range_21th - 30th', 'storey_range_> 30th', 'flat_type_1 ROOM', 'flat_type_2 ROOM', 'flat_type_3 ROOM', 'flat_type_4 ROOM', 'flat_type_5 ROOM', 'flat_type_EXECUTIVE', 'flat_type_MULTI-GENERATION']

  # #List for inputs, initalized with zeroes
  inputList = [[0]*len(colList)]

  # #Input Lists is filled with following function
  for i in range(len(colList)):
    if (colList[i] in listInput):
      inputList[0][i] +=1


  # #Output Predicted Value
  resale_value = treeReg.predict(inputList)
  print(int(resale_value))
  return(int(resale_value))