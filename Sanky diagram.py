import pandas as pd
import plotly.graph_objects as go

# Read data from CSV file
df = pd.read_csv('C:\\Users\\Hp\\Desktop\\Harshit\\book1.csv')  # put csv name and location

# Create a mapping for nodes to integers
unique_years = df['Year'].unique()
unique_calamities = df['Calamity'].unique()
unique_crop_types = df['Crop Type'].unique()
unique_crop_areas = df['Region'].unique()

# Ensure no overlap between indices for years, calamities, crop types, and crop areas
year_dict = {node: i for i, node in enumerate(unique_years)}
calamity_dict = {node: i + len(year_dict) for i, node in enumerate(unique_calamities)}
crop_type_dict = {node: i + len(year_dict) + len(calamity_dict) for i, node in enumerate(unique_crop_types)}
crop_area_dict = {node: i + len(year_dict) + len(calamity_dict) + len(crop_type_dict) for i, node in enumerate(unique_crop_areas)}

# Combine all dictionaries for easy lookup
node_dict = {**year_dict, **calamity_dict, **crop_type_dict, **crop_area_dict}

# Define sources (Year to Calamity, Calamity to Crop Type, and Crop Type to Crop Area(region/state))
sources_year_to_calamity = df['Year'].map(year_dict).tolist()
targets_year_to_calamity = df['Calamity'].map(calamity_dict).tolist()

sources_calamity_to_crop_type = df['Calamity'].map(calamity_dict).tolist()
targets_calamity_to_crop_type = df['Crop Type'].map(crop_type_dict).tolist()

sources_crop_type_to_crop_area = df['Crop Type'].map(crop_type_dict).tolist()
targets_crop_type_to_crop_area = df['Region'].map(crop_area_dict).tolist()

# Combine sources and targets
sources = (
    sources_year_to_calamity + sources_calamity_to_crop_type + sources_crop_type_to_crop_area
)
targets = (
    targets_year_to_calamity + targets_calamity_to_crop_type + targets_crop_type_to_crop_area
)

# Assuming a value of 1 for each flow for simplicity
values = [1] * len(sources)

# Define node labels
labels = list(node_dict.keys())

# Create the Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=5,
        thickness=25,
        line=dict(color="black", width=1),
        label=labels,
    ),
    link=dict(
        source=sources,
        target=targets,
        value=values,
        hovertemplate='%{source.label} to %{target.label} <br> %{value} connections',
    ))])

fig.update_layout(title_text="Sankey Diagram: Year to Calamity to Crop Type to State", font_size=10)
fig.show()
