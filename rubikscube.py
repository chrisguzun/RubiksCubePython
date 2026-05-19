import pygame
import os
import math
import random
import re

class Camera:
    def __init__(self, x, y, z, ox, oy, oz) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.ox = ox
        self.oy = oy
        self.oz = oz

class Point:
    def __init__(self,  x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z

class Piece:
    def __init__(self, verts, color) -> None:
        self.verts = verts
        self.color = color

# Color index mapping (standard Rubik's):
# 0 = White  (Y+) — Top
# 1 = Yellow (Y-) — Bottom  (opposite White)
# 2 = Red    (Z+) — Front
# 3 = Orange (Z-) — Back    (opposite Red)
# 4 = Blue   (X+) — Right
# 5 = Green  (X-) — Left    (opposite Blue)

class Rubik:
    def __init__(self) -> None:

        # 8 Corner pieces — 3 outer faces, 4 points each = 12 points
        self.corners = [

            # Top-Front-Right ( 1, 1, 1)
            Piece([
                Point( 0.5, 1.5, 0.5), Point( 1.5, 1.5, 0.5), Point( 1.5, 1.5, 1.5), Point( 0.5, 1.5, 1.5),  # White  (Y+)
                Point( 0.5, 0.5, 1.5), Point( 1.5, 0.5, 1.5), Point( 1.5, 1.5, 1.5), Point( 0.5, 1.5, 1.5),  # Red    (Z+)
                Point( 1.5, 0.5, 0.5), Point( 1.5, 1.5, 0.5), Point( 1.5, 1.5, 1.5), Point( 1.5, 0.5, 1.5),  # Blue   (X+)
            ], [colorPalette[0], colorPalette[2], colorPalette[4]]),

            # Top-Front-Left (-1, 1, 1)
            Piece([
                Point(-1.5, 1.5, 0.5), Point(-0.5, 1.5, 0.5), Point(-0.5, 1.5, 1.5), Point(-1.5, 1.5, 1.5),  # White  (Y+)
                Point(-1.5, 0.5, 1.5), Point(-0.5, 0.5, 1.5), Point(-0.5, 1.5, 1.5), Point(-1.5, 1.5, 1.5),  # Red    (Z+)
                Point(-1.5, 0.5, 0.5), Point(-1.5, 1.5, 0.5), Point(-1.5, 1.5, 1.5), Point(-1.5, 0.5, 1.5),  # Green  (X-)
            ], [colorPalette[0], colorPalette[2], colorPalette[5]]),

            # Top-Back-Right ( 1, 1,-1)
            Piece([
                Point( 0.5, 1.5,-1.5), Point( 1.5, 1.5,-1.5), Point( 1.5, 1.5,-0.5), Point( 0.5, 1.5,-0.5),  # White  (Y+)
                Point( 0.5, 0.5,-1.5), Point( 1.5, 0.5,-1.5), Point( 1.5, 1.5,-1.5), Point( 0.5, 1.5,-1.5),  # Orange (Z-)
                Point( 1.5, 0.5,-1.5), Point( 1.5, 1.5,-1.5), Point( 1.5, 1.5,-0.5), Point( 1.5, 0.5,-0.5),  # Blue   (X+)
            ], [colorPalette[0], colorPalette[3], colorPalette[4]]),

            # Top-Back-Left (-1, 1,-1)
            Piece([
                Point(-1.5, 1.5,-1.5), Point(-0.5, 1.5,-1.5), Point(-0.5, 1.5,-0.5), Point(-1.5, 1.5,-0.5),  # White  (Y+)
                Point(-1.5, 0.5,-1.5), Point(-0.5, 0.5,-1.5), Point(-0.5, 1.5,-1.5), Point(-1.5, 1.5,-1.5),  # Orange (Z-)
                Point(-1.5, 0.5,-1.5), Point(-1.5, 1.5,-1.5), Point(-1.5, 1.5,-0.5), Point(-1.5, 0.5,-0.5),  # Green  (X-)
            ], [colorPalette[0], colorPalette[3], colorPalette[5]]),

            # Bottom-Front-Right ( 1,-1, 1)
            Piece([
                Point( 0.5,-1.5, 0.5), Point( 1.5,-1.5, 0.5), Point( 1.5,-1.5, 1.5), Point( 0.5,-1.5, 1.5),  # Yellow (Y-)
                Point( 0.5,-1.5, 1.5), Point( 1.5,-1.5, 1.5), Point( 1.5,-0.5, 1.5), Point( 0.5,-0.5, 1.5),  # Red    (Z+)
                Point( 1.5,-1.5, 0.5), Point( 1.5,-0.5, 0.5), Point( 1.5,-0.5, 1.5), Point( 1.5,-1.5, 1.5),  # Blue   (X+)
            ], [colorPalette[1], colorPalette[2], colorPalette[4]]),

            # Bottom-Front-Left (-1,-1, 1)
            Piece([
                Point(-1.5,-1.5, 0.5), Point(-0.5,-1.5, 0.5), Point(-0.5,-1.5, 1.5), Point(-1.5,-1.5, 1.5),  # Yellow (Y-)
                Point(-1.5,-1.5, 1.5), Point(-0.5,-1.5, 1.5), Point(-0.5,-0.5, 1.5), Point(-1.5,-0.5, 1.5),  # Red    (Z+)
                Point(-1.5,-1.5, 0.5), Point(-1.5,-0.5, 0.5), Point(-1.5,-0.5, 1.5), Point(-1.5,-1.5, 1.5),  # Green  (X-)
            ], [colorPalette[1], colorPalette[2], colorPalette[5]]),

            # Bottom-Back-Right ( 1,-1,-1)
            Piece([
                Point( 0.5,-1.5,-1.5), Point( 1.5,-1.5,-1.5), Point( 1.5,-1.5,-0.5), Point( 0.5,-1.5,-0.5),  # Yellow (Y-)
                Point( 0.5,-1.5,-1.5), Point( 1.5,-1.5,-1.5), Point( 1.5,-0.5,-1.5), Point( 0.5,-0.5,-1.5),  # Orange (Z-)
                Point( 1.5,-1.5,-1.5), Point( 1.5,-0.5,-1.5), Point( 1.5,-0.5,-0.5), Point( 1.5,-1.5,-0.5),  # Blue   (X+)
            ], [colorPalette[1], colorPalette[3], colorPalette[4]]),

            # Bottom-Back-Left (-1,-1,-1)
            Piece([
                Point(-1.5,-1.5,-1.5), Point(-0.5,-1.5,-1.5), Point(-0.5,-1.5,-0.5), Point(-1.5,-1.5,-0.5),  # Yellow (Y-)
                Point(-1.5,-1.5,-1.5), Point(-0.5,-1.5,-1.5), Point(-0.5,-0.5,-1.5), Point(-1.5,-0.5,-1.5),  # Orange (Z-)
                Point(-1.5,-1.5,-1.5), Point(-1.5,-0.5,-1.5), Point(-1.5,-0.5,-0.5), Point(-1.5,-1.5,-0.5),  # Green  (X-)
            ], [colorPalette[1], colorPalette[3], colorPalette[5]]),
        ]

        # 12 Edge pieces — 2 outer faces, 4 points each = 8 points
        self.edges = [

            # Top-Front  ( 0, 1, 1)
            Piece([
                Point(-0.5, 1.5, 0.5), Point( 0.5, 1.5, 0.5), Point( 0.5, 1.5, 1.5), Point(-0.5, 1.5, 1.5),  # White (Y+)
                Point(-0.5, 0.5, 1.5), Point( 0.5, 0.5, 1.5), Point( 0.5, 1.5, 1.5), Point(-0.5, 1.5, 1.5),  # Red   (Z+)
            ], [colorPalette[0], colorPalette[2]]),

            # Top-Back  ( 0, 1,-1)
            Piece([
                Point(-0.5, 1.5,-1.5), Point( 0.5, 1.5,-1.5), Point( 0.5, 1.5,-0.5), Point(-0.5, 1.5,-0.5),  # White  (Y+)
                Point(-0.5, 0.5,-1.5), Point( 0.5, 0.5,-1.5), Point( 0.5, 1.5,-1.5), Point(-0.5, 1.5,-1.5),  # Orange (Z-)
            ], [colorPalette[0], colorPalette[3]]),

            # Top-Right  ( 1, 1, 0)
            Piece([
                Point( 0.5, 1.5,-0.5), Point( 1.5, 1.5,-0.5), Point( 1.5, 1.5, 0.5), Point( 0.5, 1.5, 0.5),  # White (Y+)
                Point( 1.5, 0.5,-0.5), Point( 1.5, 1.5,-0.5), Point( 1.5, 1.5, 0.5), Point( 1.5, 0.5, 0.5),  # Blue  (X+)
            ], [colorPalette[0], colorPalette[4]]),

            # Top-Left  (-1, 1, 0)
            Piece([
                Point(-1.5, 1.5,-0.5), Point(-0.5, 1.5,-0.5), Point(-0.5, 1.5, 0.5), Point(-1.5, 1.5, 0.5),  # White (Y+)
                Point(-1.5, 0.5,-0.5), Point(-1.5, 1.5,-0.5), Point(-1.5, 1.5, 0.5), Point(-1.5, 0.5, 0.5),  # Green (X-)
            ], [colorPalette[0], colorPalette[5]]),

            # Bottom-Front  ( 0,-1, 1)
            Piece([
                Point(-0.5,-1.5, 0.5), Point( 0.5,-1.5, 0.5), Point( 0.5,-1.5, 1.5), Point(-0.5,-1.5, 1.5),  # Yellow (Y-)
                Point(-0.5,-1.5, 1.5), Point( 0.5,-1.5, 1.5), Point( 0.5,-0.5, 1.5), Point(-0.5,-0.5, 1.5),  # Red    (Z+)
            ], [colorPalette[1], colorPalette[2]]),

            # Bottom-Back  ( 0,-1,-1)
            Piece([
                Point(-0.5,-1.5,-1.5), Point( 0.5,-1.5,-1.5), Point( 0.5,-1.5,-0.5), Point(-0.5,-1.5,-0.5),  # Yellow (Y-)
                Point(-0.5,-1.5,-1.5), Point( 0.5,-1.5,-1.5), Point( 0.5,-0.5,-1.5), Point(-0.5,-0.5,-1.5),  # Orange (Z-)
            ], [colorPalette[1], colorPalette[3]]),

            # Bottom-Right  ( 1,-1, 0)
            Piece([
                Point( 0.5,-1.5,-0.5), Point( 1.5,-1.5,-0.5), Point( 1.5,-1.5, 0.5), Point( 0.5,-1.5, 0.5),  # Yellow (Y-)
                Point( 1.5,-1.5,-0.5), Point( 1.5,-0.5,-0.5), Point( 1.5,-0.5, 0.5), Point( 1.5,-1.5, 0.5),  # Blue   (X+)
            ], [colorPalette[1], colorPalette[4]]),

            # Bottom-Left  (-1,-1, 0)
            Piece([
                Point(-1.5,-1.5,-0.5), Point(-0.5,-1.5,-0.5), Point(-0.5,-1.5, 0.5), Point(-1.5,-1.5, 0.5),  # Yellow (Y-)
                Point(-1.5,-1.5,-0.5), Point(-1.5,-0.5,-0.5), Point(-1.5,-0.5, 0.5), Point(-1.5,-1.5, 0.5),  # Green  (X-)
            ], [colorPalette[1], colorPalette[5]]),

            # Front-Right  ( 1, 0, 1)
            Piece([
                Point( 0.5,-0.5, 1.5), Point( 1.5,-0.5, 1.5), Point( 1.5, 0.5, 1.5), Point( 0.5, 0.5, 1.5),  # Red  (Z+)
                Point( 1.5,-0.5, 0.5), Point( 1.5,-0.5, 1.5), Point( 1.5, 0.5, 1.5), Point( 1.5, 0.5, 0.5),  # Blue (X+)
            ], [colorPalette[2], colorPalette[4]]),

            # Front-Left  (-1, 0, 1)
            Piece([
                Point(-1.5,-0.5, 1.5), Point(-0.5,-0.5, 1.5), Point(-0.5, 0.5, 1.5), Point(-1.5, 0.5, 1.5),  # Red   (Z+)
                Point(-1.5,-0.5, 0.5), Point(-1.5,-0.5, 1.5), Point(-1.5, 0.5, 1.5), Point(-1.5, 0.5, 0.5),  # Green (X-)
            ], [colorPalette[2], colorPalette[5]]),

            # Back-Right  ( 1, 0,-1)
            Piece([
                Point( 0.5,-0.5,-1.5), Point( 1.5,-0.5,-1.5), Point( 1.5, 0.5,-1.5), Point( 0.5, 0.5,-1.5),  # Orange (Z-)
                Point( 1.5,-0.5,-1.5), Point( 1.5,-0.5,-0.5), Point( 1.5, 0.5,-0.5), Point( 1.5, 0.5,-1.5),  # Blue   (X+)
            ], [colorPalette[3], colorPalette[4]]),

            # Back-Left  (-1, 0,-1)
            Piece([
                Point(-1.5,-0.5,-1.5), Point(-0.5,-0.5,-1.5), Point(-0.5, 0.5,-1.5), Point(-1.5, 0.5,-1.5),  # Orange (Z-)
                Point(-1.5,-0.5,-1.5), Point(-1.5,-0.5,-0.5), Point(-1.5, 0.5,-0.5), Point(-1.5, 0.5,-1.5),  # Green  (X-)
            ], [colorPalette[3], colorPalette[5]]),
        ]

        # 6 Center pieces — 1 outer face = 4 vertices
        self.centers = [
            Piece([Point(-0.5, 1.5,-0.5), Point( 0.5, 1.5,-0.5), Point( 0.5, 1.5, 0.5), Point(-0.5, 1.5, 0.5)], colorPalette[0]),  # White  (Y+)
            Piece([Point(-0.5,-1.5,-0.5), Point( 0.5,-1.5,-0.5), Point( 0.5,-1.5, 0.5), Point(-0.5,-1.5, 0.5)], colorPalette[1]),  # Yellow (Y-)
            Piece([Point(-0.5,-0.5, 1.5), Point( 0.5,-0.5, 1.5), Point( 0.5, 0.5, 1.5), Point(-0.5, 0.5, 1.5)], colorPalette[2]),  # Red    (Z+)
            Piece([Point(-0.5,-0.5,-1.5), Point( 0.5,-0.5,-1.5), Point( 0.5, 0.5,-1.5), Point(-0.5, 0.5,-1.5)], colorPalette[3]),  # Orange (Z-)
            Piece([Point( 1.5,-0.5,-0.5), Point( 1.5,-0.5, 0.5), Point( 1.5, 0.5, 0.5), Point( 1.5, 0.5,-0.5)], colorPalette[4]),  # Blue   (X+)
            Piece([Point(-1.5,-0.5,-0.5), Point(-1.5,-0.5, 0.5), Point(-1.5, 0.5, 0.5), Point(-1.5, 0.5,-0.5)], colorPalette[5]),  # Green  (X-)
        ]


    def rotate_side(self, side: str, angle_deg: float) -> None:
        """
        Rotate a side of the cube by any angle (in degrees).
        
        side: 'top', 'bottom', 'front', 'back', 'left', 'right'
        angle_deg: rotation angle in degrees (positive = clockwise when looking at the face)
        """

        angle = math.radians(angle_deg)
        cos_a = round(math.cos(angle), 10)
        sin_a = round(math.sin(angle), 10)

        # Map each side to its axis, rotation direction, and which coordinate/value selects pieces on that face
        side_config = {
            'top':    ('y',  1,  1.0),   # Y+ face, rotate around Y axis
            'bottom': ('y', -1, -1.0),   # Y- face, rotate around Y axis (reversed)
            'front':  ('z',  1,  1.0),   # Z+ face, rotate around Z axis
            'back':   ('z', -1, -1.0),   # Z- face, rotate around Z axis (reversed)
            'right':  ('x',  1,  1.0),   # X+ face, rotate around X axis
            'left':   ('x', -1, -1.0),   # X- face, rotate around X axis (reversed)
        }

        if side not in side_config:
            raise ValueError(f"Invalid side '{side}'. Choose from: {list(side_config.keys())}")

        axis, direction, face_coord = side_config[side]

        def rotate_point(p: Point, axis: str, cos_a: float, sin_a: float, direction: int) -> Point:
            """Rotate a single point around the given axis."""
            s = sin_a * direction  # flip rotation direction for negative faces
            x, y, z = p.x, p.y, p.z
            if axis == 'y':
                # Rotate around Y axis: X and Z change
                new_x =  x * cos_a + z * s
                new_y =  y
                new_z = -x * s     + z * cos_a
            elif axis == 'z':
                # Rotate around Z axis: X and Y change
                new_x =  x * cos_a - y * s
                new_y =  x * s     + y * cos_a
                new_z =  z
            elif axis == 'x':
                # Rotate around X axis: Y and Z change
                new_x =  x
                new_y =  y * cos_a - z * s
                new_z =  y * s     + z * cos_a
            return Point(round(new_x, 10), round(new_y, 10), round(new_z, 10))

        def piece_is_on_face(piece: Piece, axis: str, face_coord: float) -> bool:
            """Check if the piece's center lies in the face's layer."""
            coords = [getattr(p, axis) for p in piece.verts]
            center_coord = sum(coords) / len(coords)
            # The face layer spans from face_coord - 1.0 to face_coord (e.g. 0.5 to 1.5 for top)
            # Piece centers in that layer sit at face_coord * 1.0 (i.e. 1.0 or -1.0)
            return abs(center_coord - face_coord) < 0.6

        # Rotate all pieces that belong to this face
        all_pieces = self.corners + self.edges + self.centers

        for piece in all_pieces:
            if piece_is_on_face(piece, axis, face_coord):
                piece.verts = [rotate_point(p, axis, cos_a, sin_a, direction) for p in piece.verts]

def project_point(point, camera, screen_width, screen_height, fov=90):
    """
    Perspective-project a 3D point (x, y, z) into 2D screen space
    given a camera with position (x, y, z) and orientation (ox, oy, oz).
    
    Args:
        point: tuple (x, y, z)
        camera: tuple (cx, cy, cz, ox, oy, oz)
        fov: field of view in degrees
        aspect_ratio: screen width/height ratio

    Returns:
        (px, py) projected 2D coordinates (normalized)
        or None if the point is behind the camera
    """
    x, y, z = (point.x, point.y, point.z)
    cx, cy, cz, ox, oy, oz = (camera.x, camera.y, camera.z, camera.ox, camera.oy, camera.oz)

    # Translate point to camera space
    dx = x - cx
    dy = y - cy
    dz = z - cz

    # Precompute trig for orientation
    cos_yaw,   sin_yaw   = math.cos(ox), math.sin(ox)
    cos_pitch, sin_pitch = math.cos(oy), math.sin(oy)
    cos_roll,  sin_roll  = math.cos(oz), math.sin(oz)

    # ---- Rotate into camera space ----
    # Yaw
    x1 =  cos_yaw * dx + sin_yaw * dz
    z1 = -sin_yaw * dx + cos_yaw * dz

    # Pitch
    y2 =  cos_pitch * dy - sin_pitch * z1
    z2 =  sin_pitch * dy + cos_pitch * z1

    # Roll
    x3 =  cos_roll * x1 - sin_roll * y2
    y3 =  sin_roll * x1 + cos_roll * y2

    # If behind camera: skip
    if z2 >= 0:
        return None

    # ---- Perspective projection ----
    aspect = screen_width / screen_height
    f = 1 / math.tan(math.radians(fov) / 2)

    # Convert to normalized device coords (-1 to 1)
    ndc_x = (x3 * f / -z2) / aspect
    ndc_y = (y3 * f / -z2)

    # ---- Convert to pixel space ----
    px = int((ndc_x + 1) * 0.5 * screen_width)
    py = int((1 - (ndc_y + 1) * 0.5) * screen_height)  # invert Y for screen space

    return [px, py, z2]

def strokeRect(rect, color, width):
    pygame.draw.line(screen, color, rect.topleft, rect.topright, width)
    pygame.draw.line(screen, color, rect.topright, rect.bottomright, width)
    pygame.draw.line(screen, color, rect.bottomright, rect.bottomleft, width)
    pygame.draw.line(screen, color, rect.bottomleft, rect.topleft, width)

def algo(str):

    if len(str) == 0:
        return 0

    moveMap = {
        "F": "left",
        "B": "right",
        "R": "front",
        "L": "back",
        "U": "top",
        "D": "bottom"
    }

    moves = re.findall("\w'|\w", str)

    for m in moves:
        if len(m) == 2:
            rotateQueue.append([moveMap[m[0]], 90])
        else:
            rotateQueue.append([moveMap[m[0]], -90])

def reverseAlgo(str):

    if str == "":
        return ""
    
    moves = re.findall("\w'|\w", str)

    moves.reverse()

    result = ""
    for m in moves:
        if len(m) == 2:
            result += m[0]
        else:
            result += (m + "'")

    return result

def reduce(str):

    prevStr = str

    replaceDict = {}

    moves = "UDRLFB"

    for m in moves:
        replaceDict[m + m + m + "(?!')"] = m + "'"
        replaceDict[m + "'" + m + "'" + m + "'"] = m
        replaceDict[m + "'" + m + "(?!')"] = ""
        replaceDict[m + m + "'"] = ""


    for k in replaceDict:
        str = re.sub(k, replaceDict[k], str)

    if str == prevStr:
        return str
    else:
        return reduce(str)

def solve():
    
    #STEP 1 - White Cross
    pass

def renderMenu():
    pygame.draw.rect(screen, (0,0,0), menuRect)
    strokeRect(menuRect, (255,255,255), 3)
    screen.set_clip(menuRect)

    my_font = pygame.font.SysFont('charter', 20)
    for i in range(len(menuOptions)):
        text_surface = my_font.render(menuOptions[i][0], False, (255,255,255))
        screen.blit(text_surface,(menuOptions[i][1].x, menuOptions[i][1].y))
        strokeRect(pygame.Rect(menuOptions[i][1].x - 5, menuOptions[i][1].y - 1, text_surface.width + 10, text_surface.height + 10), (255,255,255), 1)

    screen.set_clip(None)

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

pygame.init()
pygame.font.init()
screenSize = (1200, 800)
screen = pygame.display.set_mode(screenSize,pygame.RESIZABLE)
clock = pygame.time.Clock()


colorPalette = [
    (255, 255, 255),#white
    (255, 213, 0),#yellow
    (183, 18, 52),#red 
    (255, 88, 0),#orange
    (0, 70, 173),#blue
    (0, 155, 72)#green
]

camera = Camera(0,0,0,0,0,0)

cameraCoords = [0,0]

cameraDist = 6

mouseFocus = False

rCube = Rubik()

rotateQueue = []

messageQueue = []

rotateSpeed = 5

totalMoves = ""

menu = False

menuRect = pygame.Rect(10,10,400,780)

menuOptions = [
    ["Shuffle"],
    ["Reset"],
    ["Instant Move"],
    ["B'DBD'B'DBUB'D'BDB'D'BU' (Corner Twist)"],
    ["UUDDRRLLFFBB (Checker Board)"],
    ["UD'RL'FB'UD' (Dot)"],
    ["U'L'U'F'RRB'RFUBBUB'LU'FURF' (Cube in a Cube in a Cube)"],
    ["UBD'FFDB'U'RRDFFD'RRDFFD'RR (Opposite Corner Twist)"],
]

my_font = pygame.font.SysFont('charter', 20)
h = 20
for o in menuOptions: #create the Rect objects for each button so it can be used with .collidePoint
    text_surface = my_font.render(o[0], False, (255,255,255))
    o.append(pygame.Rect(20,h,text_surface.width ,text_surface.height))
    h += text_surface.height + 20

maxRenderWidth = 0 #used to control menu scrolling
for m in menuOptions:
    renderWidth = my_font.render(m[0], False, (255,255,255)).width
    if maxRenderWidth < renderWidth:
        maxRenderWidth = renderWidth


running = True
while running:
    pygame.draw.rect(screen, (0,0,0), (0, 0, screenSize[0], screenSize[1]))
    screenRect = pygame.Rect(0,0,screenSize[0], screenSize[1])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not(mouseFocus) and not(menu):
                mouseFocus = True
                rel = pygame.mouse.get_rel()
                pygame.mouse.set_relative_mode(True)
            
            if menu and menuRect.collidepoint(event.pos) and event.button == 1:
                for o in menuOptions:
                    if o[1].collidepoint(event.pos):
                        messageQueue.append([o[0], 100])
                        if o[0] == "Shuffle":
                            moves = "UDRLFB"
                            a = ""
                            for i in range(0,50):
                                m = random.choice(moves)
                                if random.random() > 0.5:
                                    m += "'"
                                a += m
                            
                            algo(a)
                            totalMoves += a

                        elif o[0] == "Reset":
                            algo(reverseAlgo(reduce(totalMoves)))
                            totalMoves = ""
                        
                        elif o[0] == "Instant Move":
                            if rotateSpeed == 90:
                                rotateSpeed = 2
                            else:
                                rotateSpeed = 90

                        else:
                            algoString = o[0].split(" ")[0]
                            algo(algoString)
                            totalMoves += algoString
        
        if event.type == pygame.MOUSEMOTION:
            if mouseFocus:
                rel = pygame.mouse.get_rel()
                cameraCoords[1] += rel[1]/100
                cameraCoords[0] += rel[0]/100
        
        if event.type == pygame.MOUSEWHEEL:
            if menu:
                if menuOptions[0][1].y + (event.y * 3) > 20:
                    event.y = 0
                if menuOptions[-1][1].y + (event.y * 3) < menuRect.height - 28:
                    event.y = 0
                for m in menuOptions:
                    m[1].x += event.x * 5
                    m[1].y += event.y * 5
                    if m[1].x > 20:
                        m[1].x = 20
                    if m[1].x < menuRect.width - maxRenderWidth:
                        m[1].x = menuRect.width - maxRenderWidth

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mouseFocus = False
                rel = pygame.mouse.get_rel()
                pygame.mouse.set_relative_mode(False)
            
            if event.key == pygame.K_m:
                if menu:
                    menu = False
                    mouseFocus = True
                    rel = pygame.mouse.get_rel()
                    pygame.mouse.set_relative_mode(True)
                else:
                    menu = True
                    mouseFocus = False
                    rel = pygame.mouse.get_rel()
                    pygame.mouse.set_relative_mode(False)

            if event.key == pygame.K_w:
                rotateQueue.append(["top", -90])
                totalMoves += "U"
            
            if event.key == pygame.K_s:
                rotateQueue.append(["bottom", -90])
                totalMoves += "D"

            if event.key == pygame.K_q:
                rotateQueue.append(["right", -90])
                totalMoves += "B"
            
            if event.key == pygame.K_e:
                rotateQueue.append(["left", -90])
                totalMoves += "F"
            
            if event.key == pygame.K_a:
                rotateQueue.append(["front", -90])
                totalMoves += "R"
            
            if event.key == pygame.K_d:
                rotateQueue.append(["back", -90])
                totalMoves += "L"
    
    #move camera
    
    camera.x = math.cos(cameraCoords[1]) * cameraDist * math.cos(cameraCoords[0])
    camera.z = math.cos(cameraCoords[1]) * cameraDist * math.sin(cameraCoords[0])
    camera.y = cameraDist * math.sin(cameraCoords[1])
    
    camera.oy = cameraCoords[1]
    camera.ox = cameraCoords[0] + 1.5*math.pi

    #render cube
        
    faces = []
    
    for p in rCube.centers:
        pointsPro = []
        for v in p.verts:
            pointsPro.append(project_point(v, camera, screenSize[0], screenSize[1]))
        
        faces.append([p.color, pointsPro])
    
    for p in rCube.edges:
        pointsPro = []
        for v in p.verts:
            pointsPro.append(project_point(v, camera, screenSize[0], screenSize[1]))
        
        faces.append([p.color[0], pointsPro[0:4]])
        faces.append([p.color[1], pointsPro[4:8]])
    
    for p in rCube.corners:
        pointsPro = []
        for v in p.verts:
            pointsPro.append(project_point(v, camera, screenSize[0], screenSize[1]))
        
        faces.append([p.color[0], pointsPro[0:4]])
        faces.append([p.color[1], pointsPro[4:8]])
        faces.append([p.color[2], pointsPro[8:12]])
    
    faces.sort(key=lambda a : (a[1][0][2] + a[1][1][2] + a[1][2][2] + a[1][3][2]) / 4, reverse=False)

    for f in faces:
        points = f[1]
        pygame.draw.polygon(screen, f[0], [points[0][0:2], points[1][0:2], points[2][0:2], points[3][0:2]])
        pygame.draw.line(screen, (0,0,0), points[0][0:2], points[1][0:2], 3)
        pygame.draw.line(screen, (0,0,0), points[1][0:2], points[2][0:2], 3)
        pygame.draw.line(screen, (0,0,0), points[2][0:2], points[3][0:2], 3)
        pygame.draw.line(screen, (0,0,0), points[3][0:2], points[0][0:2], 3)
    
    
    #handle rotations
    if len(rotateQueue) > 0:
        direction = rotateSpeed * (1 if rotateQueue[0][1] > 0 else -1)
        if abs(direction) > abs(rotateQueue[0][1]):
            rCube.rotate_side(rotateQueue[0][0], rotateQueue[0][1])
            rotateQueue.pop(0)
        else:
            rCube.rotate_side(rotateQueue[0][0], direction)
            rotateQueue[0][1] = rotateQueue[0][1] - direction
    
    if menu:
        renderMenu()
    
    #display messages
    if len(messageQueue) > 0:
        my_font = pygame.font.SysFont('charter', 20)
        color = 255 * messageQueue[0][1] / 100
        text_surface = my_font.render(messageQueue[0][0], False, (color,color,color))
        screen.blit(text_surface,(600 - text_surface.width/2,700))
        messageQueue[0][1] -= 1
        if messageQueue[0][1] < 0:
            messageQueue.pop(0)

    pygame.display.flip()
    clock.tick(120)

pygame.quit()