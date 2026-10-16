"""Cut the wisdom tooth into a mesial and a distal piece and animate them coming out one at a time."""
import sys, numpy as np, trimesh
from pygltflib import GLTF2, Mesh, Node, Primitive, Attributes, Animation, AnimationChannel, AnimationChannelTarget, AnimationSampler, Accessor, BufferView, FLOAT, UNSIGNED_INT, SCALAR
src, out = sys.argv[1], sys.argv[2]
sc = trimesh.load(src, force='scene')
m = sc.geometry['wisdom tooth'].copy(); m.merge_vertices(merge_tex=True, merge_norm=True)
c = m.centroid
v = m.vertices - c; w, V = np.linalg.eigh(v.T @ v); L = V[:, 2]          # long axis
n = np.cross(L, [1, 0, 0]); n /= np.linalg.norm(n)
if n[2] < 0: n = -n                                                        # n points mesially (+z, toward the front teeth)
mes = m.slice_plane(c, n, cap=True); dis = m.slice_plane(c, -n, cap=True)
for x in (mes, dis): x.fix_normals()
print('normal', n.round(3), 'mesial', len(mes.faces), mes.is_watertight, 'distal', len(dis.faces), dis.is_watertight)

g = GLTF2().load(src)
blob = g.binary_blob()
def add(arr, typ, comp=FLOAT, target=None, mm=False):
    global blob
    blob += b'\0' * ((-len(blob)) % 4)
    g.bufferViews.append(BufferView(buffer=0, byteOffset=len(blob), byteLength=arr.nbytes, target=target))
    blob += arr.tobytes()
    kw = dict(min=arr.reshape(len(arr), -1).min(0).tolist(), max=arr.reshape(len(arr), -1).max(0).tolist()) if mm else {}
    g.accessors.append(Accessor(bufferView=len(g.bufferViews) - 1, componentType=comp, count=len(arr), type=typ, **kw))
    return len(g.accessors) - 1
mat = g.meshes[3].primitives[0].material
tooth = g.nodes[3]; tooth.mesh = None; tooth.children = []
for name, part in (('wisdom tooth mesial', mes), ('wisdom tooth distal', dis)):
    pos = np.asarray(part.vertices, np.float32); nor = np.asarray(part.vertex_normals, np.float32)
    idx = np.asarray(part.faces, np.uint32).ravel()
    prim = Primitive(attributes=Attributes(POSITION=add(pos, 'VEC3', target=34962, mm=True), NORMAL=add(nor, 'VEC3', target=34962)),
                     indices=add(idx, SCALAR, UNSIGNED_INT, target=34963), material=mat)
    g.meshes.append(Mesh(name=name, primitives=[prim]))
    g.nodes.append(Node(name=name, mesh=len(g.meshes) - 1, translation=[0, 0, 0]))
    tooth.children.append(len(g.nodes) - 1)
gap = 0.0025
t = np.array([0, 0.4, 1.4, 2.0, 3.4, 4.2, 4.8, 5.4, 6.6, 7.4, 8.0, 8.6], np.float32)
M0 = n * gap; D0 = -n * gap; z = np.zeros(3)
Dout = D0 + [0.010, 0.030, 0.002]; Dgone = Dout + [0.02, 0.10, 0]
Mmid = M0 + [0.002, 0.003, -0.006]; Mout = M0 + [0.010, 0.030, -0.004]; Mgone = Mout + [0.02, 0.10, 0]
dis_k = [z, z, D0, D0, Dout, Dout, Dgone, Dgone, Dgone, Dgone, Dgone, Dgone]
mes_k = [z, z, M0, M0, M0, M0, M0, Mmid, Mout, Mout, Mgone, Mgone]
ti = add(t, SCALAR, mm=True)
samplers, channels = [], []
for k, node in ((mes_k, tooth.children[0]), (dis_k, tooth.children[1])):
    samplers.append(AnimationSampler(input=ti, output=add(np.array(k, np.float32), 'VEC3'), interpolation='LINEAR'))
    channels.append(AnimationChannel(sampler=len(samplers) - 1, target=AnimationChannelTarget(node=node, path='translation')))
g.animations = [Animation(name='extraction', samplers=samplers, channels=channels)]
g.buffers[0].byteLength = len(blob); g.set_binary_blob(blob); g.save_binary(out)
print('saved', out, len(blob))
