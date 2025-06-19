from dotenv import load_dotenv  # added to load env variables
import os                       # added for env var support
load_dotenv(dotenv_path=".env.local")  # load env variables

PROJECT_ID = os.environ.get("PROJECT_ID")  # get project id from env

import ee
ee.Initialize(project=PROJECT_ID)  # modified to load project id from env

# # ✅ Use new harmonized dataset
# collection = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
#     .filterDate('2025-6-10', '2025-06-18') \
#     .filterBounds(ee.Geometry.Point([78.0421, 27.1751]))  # e.g., Taj Mahal

# image = collection.first()
# print(image.getInfo())

# import ee
# import geemap
# import matplotlib.pyplot as plt

# # Initialize Earth Engine
# ee.Initialize()

# # Load the Sentinel-2 image by ID
# image = ee.Image('COPERNICUS/S2_SR_HARMONIZED/20250612T052649_20250612T053352_T43RGL')

# # Select RGB bands for true color
# rgb_image = image.select(['B4', 'B3', 'B2'])

# # Define visualization parameters
# vis_params = {
#     'min': 0,
#     'max': 3000,
#     'bands': ['B4', 'B3', 'B2']
# }

# # Define region of interest (footprint of the image)
# region = image.geometry()

# # Get a thumbnail URL
# url = rgb_image.getThumbURL({
#     'dimensions': 1024,
#     'region': region,
#     'format': 'png',
#     'min': 0,
#     'max': 3000,
#     'bands': ['B4', 'B3', 'B2']
# })

# print("🖼️ Image thumbnail URL (open in browser):\n", url)

# # Optional: Download and show the image in Python
# import requests
# from PIL import Image
# from io import BytesIO

# response = requests.get(url)
# img = Image.open(BytesIO(response.content))

# # Show image in a matplotlib viewer
# plt.imshow(img)
# plt.axis('off')
# plt.title("Sentinel-2 True Color Composite")
# plt.show()

# # Optional: Save it locally
# img.save("sentinel2_true_color.png")
# print("✅ Image saved as 'sentinel2_true_color.png'")
# import ee
# ee.Initialize(project=PROJECT_ID)  # modified to load project id from env

# # Define location (Taj Mahal example)
# point = ee.Geometry.Point([78.0421, 27.1751])

# # Load Sentinel-2 SR Harmonized data
# collection = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
#     .filterDate('2025-06-10', '2025-06-18') \
#     .filterBounds(point)

# # NDVI Calculation Function
# def compute_ndvi(image):
#     ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
#     image_with_ndvi = image.addBands(ndvi)
#     return image_with_ndvi.set({'NDVI_mean': ndvi.reduceRegion(
#         reducer=ee.Reducer.mean(),
#         geometry=point.buffer(100),  # 100m radius around point
#         scale=10,
#         maxPixels=1e8
#     ).get('NDVI')})

# # Map NDVI calculation across the collection
# collection_with_ndvi = collection.map(compute_ndvi)

# # Get list of images with their NDVI values
# ndvi_list = collection_with_ndvi.aggregate_array('NDVI_mean').getInfo()
# id_list = collection_with_ndvi.aggregate_array('system:index').getInfo()

# # Print NDVI per image
# for img_id, ndvi in zip(id_list, ndvi_list):
#     print(f"{img_id}: NDVI = {ndvi}")
# import ee
# ee.Initialize(project=PROJECT_ID)  # modified to load project id from env

point = ee.Geometry.Point([78.0421, 27.1751])

collection = ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED") \
    .filterDate('2025-06-10', '2025-06-18') \
    .filterBounds(point)

# ✅ Define Index Functions
def add_indices(image):
    ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI')
    evi = image.expression(
        '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))',
        {'NIR': image.select('B8'), 'RED': image.select('B4'), 'BLUE': image.select('B2')}
    ).rename('EVI')
    savi = image.expression(
        '((NIR - RED) / (NIR + RED + 0.5)) * 1.5',
        {'NIR': image.select('B8'), 'RED': image.select('B4')}
    ).rename('SAVI')
    gci = image.expression(
        '(NIR / GREEN) - 1',
        {'NIR': image.select('B8'), 'GREEN': image.select('B3')}
    ).rename('GCI')
    ndwi = image.normalizedDifference(['B3', 'B8']).rename('NDWI')
    msi = image.expression(
        'SWIR / NIR',
        {'SWIR': image.select('B11'), 'NIR': image.select('B8')}
    ).rename('MSI')
    ndmi = image.normalizedDifference(['B8', 'B11']).rename('NDMI')
    nbr = image.normalizedDifference(['B8', 'B12']).rename('NBR')
    rendvi = image.normalizedDifference(['B8', 'B5']).rename('RENDVI')

    # Mean values in 100m buffer
    indices = ee.Image.cat([ndvi, evi, savi, gci, ndwi, msi, ndmi, nbr, rendvi])
    stats = indices.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=point.buffer(100),
        scale=10,
        maxPixels=1e8
    )

    return image.set(stats)

# ✅ Add indices and extract metadata
def enrich_image(image):
    image = add_indices(image)
    meta_props = [
        'CLOUD_COVERAGE_ASSESSMENT',
        'SNOW_ICE_PERCENTAGE',
        'VEGETATION_PERCENTAGE',
        'NOT_VEGETATED_PERCENTAGE',
        'WATER_PERCENTAGE'
    ]
    return image.set({p: image.get(p) for p in meta_props})

# ✅ Apply function to all images
enriched = collection.map(enrich_image)

# ✅ Print summary
props = enriched.aggregate_array('system:index').getInfo()
ndvi = enriched.aggregate_array('NDVI').getInfo()
evi = enriched.aggregate_array('EVI').getInfo()
savi = enriched.aggregate_array('SAVI').getInfo()
gci = enriched.aggregate_array('GCI').getInfo()
cloud = enriched.aggregate_array('CLOUD_COVERAGE_ASSESSMENT').getInfo()

# ✅ Print everything
for i in range(len(props)):
    print(f"\n🛰️ Image: {props[i]}")
    print(f"  NDVI: {ndvi[i]}")
    print(f"  EVI: {evi[i]}")
    print(f"  SAVI: {savi[i]}")
    print(f"  GCI: {gci[i]}")
    print(f"  Cloud Cover: {cloud[i]}%")
