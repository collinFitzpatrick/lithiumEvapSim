import os

# 1. Configuration
# time_points = [0.1, 10, 20, 30, 40] # for ramp up
# offset = 0
# time_points = [40.2, 40.4, 40.6, 40.8, 41.0] # for steady
# offset = 40
# for cooldown
time_points = {0:list(range(0, 150, 1)),
1:[150.5, 151, 151.5, 152, 152.5,153,  153.5, 154, 154.5, 155],
2:list(range(156, 255, 1)),
3:list(range(256, 1346, 10))} 
offsets = [0, 150,155, 255]

output_dir = r'C:\Users\cfitzpat\Documents\LVD\lithiumEvapSim'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 2. Access the Model
model = ExtAPI.DataModel.Project.Model
# Change this subscript to access different Solutions!
# 0 for ramp up, 1 for steady, 2 for cooldown
for i in [1]:
    section_times = time_points[i]
    offset = offsets[i]
    analysis = model.Analyses[i]
    solution = analysis.Solution
    
    # 3. Create a temporary Named Selection
    ns_group = model.NamedSelections
    new_ns = ns_group.AddNamedSelection()
    new_ns.Name = "TEMP_EXPORT_NS"
    
    # Get all Body IDs
    all_bodies = model.GetChildren(DataModelObjectCategory.Body, True)
    body_ids = [b.GetGeoBody().Id for b in all_bodies]
    
    # Use the internal CreateSelection method to avoid the 'read-only' error
    new_selection = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
    new_selection.Ids = body_ids
    new_ns.Location = new_selection
    
    print("Created Named Selection for all bodies.")
    
    # 4. Create the Result Object
    temp_result = solution.AddTemperature()
    temp_result.Name = "TEMP_EXPORT_RESULT"
    temp_result.Location = new_ns
    
    # 5. Loop and Export
    for t in section_times:
        temp_result.DisplayTime = Quantity(t-offset, "s")
        temp_result.EvaluateAllResults()
        
        file_path = os.path.join(output_dir, "fullShotNewMesh5sSteady_{}s.csv".format(t))
        temp_result.ExportToTextFile(file_path)
        print("Successfully exported: " + file_path)
    
    # 6. CLEANUP
    temp_result.Delete()
    new_ns.Delete()
    
    print("--- Export Complete & Tree Cleaned ---")
'''NOTE : All workflows will not be recorded, as recording is under development.'''


#region Details View Action
ansys_analysis_settings_647 = DataModel.GetObjectById(647)
step_index_list = [1]
with Transaction():
    for step_index in step_index_list:
        ansys_analysis_settings_647.SetMaximumTimeStep(step_index, Quantity(1, "sec"))
#endregion

#region Details View Action
ansys_analysis_settings_647 = DataModel.GetObjectById(647)
step_index_list = [1]
with Transaction():
    for step_index in step_index_list:
        ansys_analysis_settings_647.SetMaximumTimeStep(step_index, Quantity(10, "sec"))
#endregion
