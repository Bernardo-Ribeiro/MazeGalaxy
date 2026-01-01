from Range import *
from collections import OrderedDict
import random
from mathutils import Vector

class MazeBuilder(types.KX_PythonComponent):
    args = OrderedDict([
        ("level", 1),
        ("cell_size", 2),
        ("wall_thickness", 0.2),
        ("wall_height", 1),
        ("wall_material", ""),
    ])
    def awake(self, args):
        self.grid = []
        self.stack = []
        self.current = None
        self.generated = False
        self.mesh_builder = None
        self.exit_position = None
        self.start_position = None

    def start(self, args):
        self.scene = logic.getCurrentScene()

        self.level = max(1, int(args.get("nivel", 1)))
        base = 6
        self.rows = base + self.level * 2
        self.cols = base + self.level * 2

        self.cell_size = max(0.1, float(args["cell_size"]))
        self.wall_thickness = max(0.05, float(args["wall_thickness"]))
        self.wall_height = max(0.1, float(args["wall_height"]))
        self.wall_material = args.get("wall_material", "")

        self.create_grid()
        self.current = self.grid[0]
        self.reGenerate()

    def create_grid(self):
        self.grid = []
        for y in range(self.rows):
            for x in range(self.cols):
                self.grid.append({
                    'x': x, 'y': y,
                    'walls': {'top': True, 'right': True, 'bottom': True, 'left': True},
                    'visited': False
                })

    def index(self, x, y):
        if 0 <= x < self.cols and 0 <= y < self.rows:
            return self.grid[y * self.cols + x]
        return None

    def reGenerate(self):
        if self.generated:
            self.reset_maze()
            self.level += 1
            base = 6
            self.rows = base + self.level * 2
            self.cols = base + self.level * 2
            print(f"[MazeBuilder] Nível {self.level} - Tamanho: {self.rows} x {self.cols}")

            self.create_grid()

        for cell in self.grid:
            cell['visited'] = False
            cell['walls'] = {'top': True, 'right': True, 'bottom': True, 'left': True}

        self.current = self.grid[0]
        self.generate_maze()
        self.build_mesh()
        self.generated = True
        
    def get_level(self):
        return self.level
    
    def regenerate_current_level(self):
        """Regenera o labirinto atual mantendo o mesmo nível"""
        # Não incrementar o nível, apenas regenerar
        if self.generated:
            self.reset_maze()
            # NÃO mudar self.level aqui!
            print(f"[MazeBuilder] Regenerando Nível {self.level} - Tamanho: {self.rows} x {self.cols}")
        
        # Resetar visitados e paredes
        for cell in self.grid:
            cell['visited'] = False
            cell['walls'] = {'top': True, 'right': True, 'bottom': True, 'left': True}

        self.current = self.grid[0]
        self.generate_maze()
        self.build_mesh()
        self.generated = True

    def generate_maze(self):
        self.stack = [self.current]
        self.current['visited'] = True

        entrance_cell = self.index(random.randint(0, self.cols - 1), 0)
        exit_cell = self.index(random.randint(0, self.cols - 1), self.rows - 1)

        entrance_cell['walls']['top'] = False
        exit_cell['walls']['bottom'] = False

        entrance_cell['visited'] = False  
        exit_cell['visited'] = False       

        while self.stack:
            neighbors = self.get_unvisited_neighbors(self.current)
            if neighbors:
                next_cell = random.choice(neighbors)
                self.remove_walls(self.current, next_cell)
                self.stack.append(self.current)
                self.current = next_cell
                self.current['visited'] = True
            else:
                self.current = self.stack.pop()

        for i in range(self.cols):
            cell = entrance_cell
            if cell:
                cell['walls']['bottom'] = False

        for i in range(self.cols):
            cell = exit_cell
            if cell:
                cell['walls']['top'] = False
                
                
        self.exit_position = Vector((exit_cell['x'] * self.cell_size, exit_cell['y'] * self.cell_size, 0))
        self.start_position = Vector((entrance_cell['x'] * self.cell_size, entrance_cell['y'] * self.cell_size, 0))
            
    def get_exit_position(self):
        return self.exit_position
    
    def get_start_position(self):
        return self.start_position
    
    def get_unvisited_neighbors(self, cell):
        x, y = cell['x'], cell['y']
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []

        for dx, dy in directions:
            neighbor = self.index(x + dx, y + dy)
            if neighbor and not neighbor['visited']:
                neighbors.append(neighbor)
        return neighbors

    def remove_walls(self, a, b):
        dx = a['x'] - b['x']
        dy = a['y'] - b['y']

        if dx == 1:
            a['walls']['left'] = False
            b['walls']['right'] = False
        elif dx == -1:
            a['walls']['right'] = False
            b['walls']['left'] = False
        elif dy == 1:
            a['walls']['bottom'] = False
            b['walls']['top'] = False
        elif dy == -1:
            a['walls']['top'] = False
            b['walls']['bottom'] = False

    def build_mesh(self):
        self.mesh_builder = types.KX_MeshBuilder("MazeMesh", self.scene)

        if self.wall_material:
            material = self.scene.materials.get(self.wall_material, None)
        else:
            material = self.object.meshes[0].materials[0] if self.object.meshes else None

        if not material:
            print("[MazeBuilder] Material não encontrado.")
            return

        slot = self.mesh_builder.addSlot(material, 0)

        cs = self.cell_size
        wt = self.wall_thickness
        wh = self.wall_height

        vertices = []
        indices = []
        vertex_offset = 0

        for cell in self.grid:
            x = cell['x'] * cs
            y = cell['y'] * cs

            for side in ['top', 'bottom', 'left', 'right']:
                if cell['walls'][side]:
                    if side == 'top':
                        px, py = x, y + cs / 2
                        w, t = cs, wt
                    elif side == 'bottom':
                        px, py = x, y - cs / 2
                        w, t = cs, wt
                    elif side == 'left':
                        px, py = x - cs / 2, y
                        w, t = wt, cs
                    elif side == 'right':
                        px, py = x + cs / 2, y
                        w, t = wt, cs

                    v_count = self.add_wall_data(vertices, px, py, w, t, wh, side)
                    for i in range(0, v_count, 4):
                        indices.append((vertex_offset + i, vertex_offset + i + 1, vertex_offset + i + 2))
                        indices.append((vertex_offset + i, vertex_offset + i + 2, vertex_offset + i + 3))


                    vertex_offset += v_count

        if hasattr(slot, 'addVerticesBatch'):
            slot.addVerticesBatch(vertices)
        else:
            for vertex in vertices:
                slot.addVertex(vertex['pos'], normal=vertex['normal'])

        for tri in indices:
            slot.addIndex(tri)

        mesh = self.mesh_builder.finish()
        self.object.replaceMesh(mesh, 1, 0)
        self.object.reinstancePhysicsMesh(dupli=False)

        center_x = -(self.cols * cs) / 2
        center_y = -(self.rows * cs) / 2
        self.object.localPosition = (center_x, center_y, 0)

    def add_wall_data(self, vertices, x, y, width, thickness, height, side):
        """Cria uma parede como uma caixa (paralelepípedo com 6 lados)"""
        half_w = width / 2
        half_t = thickness / 2

        min_x, max_x = x - half_w, x + half_w
        min_y, max_y = y - half_t, y + half_t
        min_z, max_z = 0, height

        # Vértices (8 cantos do paralelepípedo)
        v = [
            (min_x, min_y, min_z),  # 0
            (max_x, min_y, min_z),  # 1
            (max_x, max_y, min_z),  # 2
            (min_x, max_y, min_z),  # 3
            (min_x, min_y, max_z),  # 4
            (max_x, min_y, max_z),  # 5
            (max_x, max_y, max_z),  # 6
            (min_x, max_y, max_z),  # 7
        ]

        faces = [
            # Frente
            ((0, 1, 5, 4), (0, -1, 0)),
            # Trás
            ((2, 3, 7, 6), (0, 1, 0)),
            # Direita
            ((1, 2, 6, 5), (1, 0, 0)),
            # Esquerda
            ((3, 0, 4, 7), (-1, 0, 0)),
            # Topo
            ((4, 5, 6, 7), (0, 0, 1)),
            # Base
            ((0, 3, 2, 1), (0, 0, -1)),
        ]

        start_index = len(vertices)
        for quad, normal in faces:
            v0, v1, v2, v3 = [v[i] for i in quad]
            vertices.extend([
                {'pos': v0, 'normal': normal},
                {'pos': v1, 'normal': normal},
                {'pos': v2, 'normal': normal},
                {'pos': v3, 'normal': normal},
            ])
        return 24


    def reset_maze(self):
        if self.mesh_builder:
            self.mesh_builder = None

    def update(self):
        pass
