import numpy as np
from generate_scene import get_ball
import matplotlib.pyplot as plt

# specular exponent
k_e = 50

def render(Z, N, A, S, 
           point_light_loc, point_light_strength, 
           directional_light_dirn, directional_light_strength,
           ambient_light, k_e):
  # To render the images you will need the camera parameters, you can assume
  # the following parameters. (cx, cy) denote the center of the image (point
  # where the optical axis intersects with the image, f is the focal length.
  # These parameters along with the depth image will be useful for you to
  # estimate the 3D points on the surface of the sphere for computing the
  # angles between the different directions.
  h, w = A.shape
  cx, cy = w / 2, h /2
  f = 128.

  # Ambient Term
  I = A * ambient_light
  # Get the camera coordinates of all the points in the pixel coordinates
  coordinates = np.zeros((h, w, 3))
  for y in range(h):
    for x in range(w):
      depth = Z[y, x]
      coord = [(x - cx) * depth / f, (y - cy) * depth / f, depth]
      coordinates[y, x, :] = np.array(coord)

  # Normalize the directional light
  directional_light_dirn = np.array(directional_light_dirn) / np.linalg.norm(np.array(directional_light_dirn))


  
  # Diffuse Term
  direction_vec_of_point_light = np.array(point_light_loc) - coordinates
  point_diffuse = np.sum(direction_vec_of_point_light * N, axis=2)
  direction_vec_of_point_light = (direction_vec_of_point_light.T / np.linalg.norm(direction_vec_of_point_light, axis=2).T).T

  point_diffuse = np.sum(direction_vec_of_point_light * N, axis=2)
  dir_diffuse = np.sum(directional_light_dirn * N, axis=2)

  #Remove any negative values from the diffuse matrix.
 
  point_diffuse[point_diffuse < 0] = 0
  dir_diffuse[dir_diffuse < 0] = 0
  diffu_term = point_diffuse * np.array(point_light_strength)
  diffu_term += dir_diffuse * np.array(directional_light_strength)
  diffu_term = A * diffu_term
  I += diffu_term

  # Specular Term

  # acquire the viewing instructions, then normalize
  vector = np.zeros(3) - coordinates
  vector = (vector.T / np.linalg.norm(vector, axis=2).T).T


  point_ref = (2 * np.sum(direction_vec_of_point_light * N, axis=2).T * N.T).T - direction_vec_of_point_light
  dir_ref = (2 * np.sum(directional_light_dirn * N, axis=2).T * N.T).T - directional_light_dirn

  # Get the specular matrices
  specular_point = np.sum(point_ref * vector, axis=2)
  dir_spec = np.sum(dir_ref * vector, axis=2)

  # Remove all negative numbers from the specular matrices.
  specular_point[specular_point < 0] = 0
  dir_spec[dir_spec < 0] = 0

  I += S * (np.array(point_light_strength) * (specular_point) ** k_e + np.array(directional_light_strength) * (
    dir_spec) ** k_e)

  I = np.minimum(I, 1)*255
  I = I.astype(np.uint8)
  I = np.repeat(I[:,:,np.newaxis], 3, axis=2)
  return I


def main():
  for specular in [True, False]:
    # get_ball function returns:
    # - Z (depth image: distance to scene point from camera center, along the
    # Z-axis)
    # - N is the per pixel surface normals (N[:,:,0] component along X-axis
    # (pointing right), N[:,:,1] component along Y-axis (pointing down),
    # N[:,:,2] component along Z-axis (pointing into the scene)),
    # - A is the per pixel ambient and diffuse reflection coefficient per pixel,
    # - S is the per pixel specular reflection coefficient.
    Z, N, A, S = get_ball(specular=specular)

    # Strength of the ambient light.
    ambient_light = 0.5

    # For the following code, you can assume that the point sources are located
    # at point_light_loc and have a strength of point_light_strength. For the
    # directional light sources, you can assume that the light is coming _from_
    # the direction indicated by directional_light_dirn (i.e., \hat{v}_i =
    # directional_light_dirn), and with strength directional_light_strength.
    # The coordinate frame is centered at the camera, X axis points to the
    # right, Y-axis point down, and Z-axis points into the scene.

    # Case I: No directional light, only point light source that moves around
    # the object.
    point_light_strength = [1.5]
    directional_light_dirn = [[1, 0, 0]]
    directional_light_strength = [0.0]

    fig, axes = plt.subplots(4, 4, figsize=(15, 10))
    axes = axes.ravel()[::-1].tolist()
    for theta in np.linspace(0, np.pi * 2, 16):
      point_light_loc = [[10 * np.cos(theta), 10 * np.sin(theta), -3]]
      I = render(Z, N, A, S, point_light_loc, point_light_strength,
                 directional_light_dirn, directional_light_strength,
                 ambient_light, k_e)
      ax = axes.pop()
      ax.imshow(I)
      ax.set_axis_off()
    plt.savefig(f'specular{specular:d}_move_point.png', bbox_inches='tight')
    plt.close()

    # Case II: No point source, just a directional light source that moves
    # around the object.
    point_light_loc = [[0, -10, 2]]
    point_light_strength = [0.0]
    directional_light_strength = [2.5]

    fig, axes = plt.subplots(4, 4, figsize=(15, 10))
    axes = axes.ravel()[::-1].tolist()
    for theta in np.linspace(0, np.pi * 2, 16):
      directional_light_dirn = [np.array([np.cos(theta), np.sin(theta), .1])]
      directional_light_dirn[0] = \
        directional_light_dirn[0] / np.linalg.norm(directional_light_dirn[0])
      I = render(Z, N, A, S, point_light_loc, point_light_strength,
                 directional_light_dirn, directional_light_strength,
                 ambient_light, k_e)
      ax = axes.pop()
      ax.imshow(I)
      ax.set_axis_off()
    plt.savefig(f'specular{specular:d}_move_direction.png', bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
  main()
