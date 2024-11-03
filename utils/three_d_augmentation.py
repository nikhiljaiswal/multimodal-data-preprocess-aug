import numpy as np
import trimesh
import os
from scipy.spatial.transform import Rotation

def load_off_file(file_path):
    """Load OFF file and return vertices and faces"""
    mesh = trimesh.load(file_path)
    return mesh.vertices, mesh.faces

def save_off_file(vertices, faces, output_path):
    """Save vertices and faces as OFF file"""
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    mesh.export(output_path)
    return output_path

def rotation(file_path):
    """
    Apply random rotation to the 3D model
    """
    try:
        vertices, faces = load_off_file(file_path)
        
        # Generate random rotation angles
        angles = np.random.uniform(0, 360, 3)  # Random angles for x, y, z axes
        rotation = Rotation.from_euler('xyz', angles, degrees=True)
        
        # Apply rotation
        rotated_vertices = rotation.apply(vertices)
        
        # Save the rotated mesh
        output_path = os.path.join(os.path.dirname(file_path), 'rotated_' + os.path.basename(file_path))
        save_off_file(rotated_vertices, faces, output_path)
        
        return output_path
    except Exception as e:
        return f"Error in rotation: {str(e)}"

def scaling(file_path):
    """
    Apply random scaling to the 3D model
    """
    try:
        vertices, faces = load_off_file(file_path)
        
        # Generate random scale factors for each axis
        scale_factors = np.random.uniform(0.5, 1.5, 3)  # Random scale between 0.5 and 1.5
        
        # Apply scaling
        scaled_vertices = vertices * scale_factors
        
        # Save the scaled mesh
        output_path = os.path.join(os.path.dirname(file_path), 'scaled_' + os.path.basename(file_path))
        save_off_file(scaled_vertices, faces, output_path)
        
        return output_path
    except Exception as e:
        return f"Error in scaling: {str(e)}"

def adding_noise(file_path):
    """
    Add random noise to vertex positions
    """
    try:
        vertices, faces = load_off_file(file_path)
        
        # Calculate model scale for appropriate noise magnitude
        model_scale = np.max(np.abs(vertices))
        noise_magnitude = model_scale * 0.02  # 2% of model scale
        
        # Generate and apply random noise
        noise = np.random.normal(0, noise_magnitude, vertices.shape)
        noisy_vertices = vertices + noise
        
        # Save the noisy mesh
        output_path = os.path.join(os.path.dirname(file_path), 'noisy_' + os.path.basename(file_path))
        save_off_file(noisy_vertices, faces, output_path)
        
        return output_path
    except Exception as e:
        return f"Error in adding noise: {str(e)}"