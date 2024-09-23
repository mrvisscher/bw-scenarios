import bw2calc as bc
import bw2data as bd
import matrix_utils as mu
import bw_processing as bp
from fs.zipfs import ZipFS

bd.projects.set_current("playground")

lca = bc.LCA({("garden", "act_0"): 1}, method=('method_0',))
lca.lci()
lca.lcia()
print(lca.score)
