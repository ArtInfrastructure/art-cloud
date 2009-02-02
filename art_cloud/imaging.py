# Copyright 2009 Trevor F. Smith Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
import Image

# taken from django example at http://code.djangoproject.com/attachment/wiki/CustomUploadAndFilters/imaging.py

def fit(file_path, max_width=None, max_height=None, save_as=None):
    # Open file
    img = Image.open(file_path)
    
    # Store original image width and height
    w, h = img.size
    
    # Replace width and height by the maximum values
    w = int(max_width or w)
    h = int(max_height or h)
    
    # Proportinally resize
    img.thumbnail((w, h), Image.ANTIALIAS)
    
    # Save in (optional) 'save_as' or in the original path
    img.save(save_as or file_path)
    
    return True

def fit_crop(file_path, max_width=None, max_height=None, save_as=None):
    # Open file
    img = Image.open(file_path)
    
    # Store original image width and height
    w, h = float(img.size[0]), float(img.size[1])
    
    # Use the original size if no size given
    max_width = float(max_width or w)
    max_height = float(max_height or h)
    
    # Find the closest bigger proportion to the maximum size
    scale = max(max_width / w, max_height / h)
    
    # Image bigger than maximum size?
    if (scale < 1):
        # Calculate proportions and resize
        w = int(w * scale)
        h = int(h * scale)
        img = img.resize((w, h), Image.ANTIALIAS)
    #
    
    # Avoid enlarging the image
    max_width = min(max_width, w)
    max_height = min(max_height, h)
    
    # Define the cropping box
    left = int((w - max_width) / 2)
    top = int((h - max_height) / 2)
    right = int(left + max_width)
    bottom = int(top + max_height)
    
    # Crop to fit the desired size
    img = img.crop( (left, top, right, bottom) )
    
    # Save in (optional) 'save_as' or in the original path
    img.save(save_as or file_path)
    
    return True
