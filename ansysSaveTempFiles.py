import os

# 1. Configuration
time_points = [0.1, 10, 20, 30, 40] # for ramp up
offset = 0
# time_points = [4021, 40.4, 40.6, 40.8, 41.0] # for steady
# offset = 40
# for cooldown
# time_points = [51, 60, 70, 80, 90, 100, 200, 300, 400, 500, 700, 900, 1100, 1241] # for ramp up
# offset = 41

output_dir = r'C:\Users\cfitzpat\Documents\LVD\lithiumEvapSim'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 2. Access the Model
model = ExtAPI.DataModel.Project.Model
# Change this subscript to access different Solutions!
# 0 for ramp up, 1 for steady, 2 for cooldown
analysis = model.Analyses[0]
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
for t in time_points:
    temp_result.DisplayTime = Quantity(t-offset, "s")
    temp_result.EvaluateAllResults()
    
    file_path = os.path.join(output_dir, "fullShot1sSteadyHalfPower_{}s.csv".format(t))
    temp_result.ExportToTextFile(file_path)
    print("Successfully exported: " + file_path)

# 6. CLEANUP
temp_result.Delete()
new_ns.Delete()

print("--- Export Complete & Tree Cleaned ---")