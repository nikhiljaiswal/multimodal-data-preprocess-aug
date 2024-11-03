import numpy as np
import trimesh
import os

def load_off_file(file_path):
    """Load OFF file and return vertices and faces"""
    mesh = trimesh.load(file_path)
    return mesh.vertices, mesh.faces

def save_off_file(vertices, faces, output_path):
    """Save vertices and faces as OFF file"""
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            # Write OFF header
            f.write('OFF\n')
            # Write number of vertices, faces, and edges (0 for edges)
            f.write(f'{len(vertices)} {len(faces)} 0\n')
            # Write vertices
            for v in vertices:
                f.write(f'{v[0]} {v[1]} {v[2]}\n')
            # Write faces
            for face in faces:
                f.write(f'{len(face)} {" ".join(map(str, face))}\n')
        return output_path
    except Exception as e:
        return f"Error saving file: {str(e)}"

def normalization(file_path):
    """
    Normalize the 3D model to have unit scale
    """
    try:
        vertices, faces = load_off_file(file_path)
        
        # Calculate the scale factor
        scale_factor = np.max(np.abs(vertices))
        if scale_factor == 0:
            return "Error: Invalid model - zero scale factor"
        
        # Normalize vertices
        normalized_vertices = vertices / scale_factor
        
        # Save in the same directory as input file
        output_path = os.path.join(os.path.dirname(file_path), 'normalized_' + os.path.basename(file_path))
        print(f"Saving normalized file to: {output_path}")  # Debug print
        result = save_off_file(normalized_vertices, faces, output_path)
        
        # Verify file was saved
        if os.path.exists(output_path):
            print(f"File successfully saved at {output_path}")
        else:
            print(f"File not found at {output_path}")
            
        return output_path
    except Exception as e:
        print(f"Error in normalization: {str(e)}")  # Debug print
        return f"Error in normalization: {str(e)}"

def centering(file_path):
    """
    Center the 3D model at origin (0,0,0)
    """
    try:
        vertices, faces = load_off_file(file_path)
        
        # Calculate center of mass
        center = np.mean(vertices, axis=0)
        
        # Center vertices
        centered_vertices = vertices - center
        
        # Save the centered mesh
        output_path = os.path.join(os.path.dirname(file_path), 'centered_' + os.path.basename(file_path))
        save_off_file(centered_vertices, faces, output_path)
        
        return output_path
    except Exception as e:
        return f"Error in centering: {str(e)}" 