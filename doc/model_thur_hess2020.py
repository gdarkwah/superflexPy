import sys
import pathlib
REPO_FOLDER = pathlib.Path(__file__).absolute().parents[2]
sys.path.insert(0, str(REPO_FOLDER))
from superflexpy.implementation.elements.thur_model_hess import SnowReservoir, UnsaturatedReservoir, HalfTriangularLag, FastReservoir
from superflexpy.implementation.elements.structure_elements import Transparent, Junction, Splitter
from superflexpy.framework.unit import Unit
from superflexpy.framework.node import Node
from superflexpy.framework.network import Network
from superflexpy.implementation.computation.pegasus_root_finding import PegasusPython


# Declare the elements
solver = PegasusPython()

# Fluxes in the order P, T, PET
upper_splitter = Splitter(
    direction=[
        [0, 1, None],    # P and T go to the snow reservoir
        [2, None, None]  # PET goes to the transparent element
    ],
    weight=[
        [1.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ],
    id='upper-splitter'
)

snow = SnowReservoir(
    parameters={'t0': 0.0, 'k': 0.01, 'm': 2.0},
    states={'S0': 0.0},
    solver=solver,
    id='snow'
)

upper_transparent = Transparent(
    id='upper-transparent'
)

upper_junction = Junction(
    direction=[
        [0, None],
        [None, 0]
    ],
    id='upper-junction'
)

unsaturated = UnsaturatedReservoir(
    parameters={'Smax': 50.0, 'Ce': 1.0, 'm': 0.01, 'beta': 2.0},
    states={'S0': 10.0},
    solver=solver,
    id='unsaturated'
)

lower_splitter = Splitter(
    direction=[
        [0],
        [0]
    ],
    weight=[
        [0.3],   # Portion to slow reservoir
        [0.7]    # Portion to fast reservoir
    ],
    id='lower-splitter'
)

lag_fun = HalfTriangularLag(
    parameters={'lag-time': 2.0},
    states={'lag': None},
    id='lag-fun'
)

fast = FastReservoir(
    parameters={'k': 0.01, 'alpha': 3.0},
    states={'S0': 0.0},
    solver=solver,
    id='fast'
)

slow = FastReservoir(
    parameters={'k': 1e-4, 'alpha': 1.0},
    states={'S0': 0.0},
    solver=solver,
    id='slow'
)

lower_transparent = Transparent(
    id='lower-transparent'
)

lower_junction = Junction(
    direction=[
        [0, 0]
    ],
    id='lower-junction'
)

# Create the HRUs
consolidated = Unit(
    layers=[
        [upper_splitter],
        [snow, upper_transparent],
        [upper_junction],
        [unsaturated],
        [lower_splitter],
        [slow, lag_fun],
        [lower_transparent, fast],
        [lower_junction],
    ],
    id='consolidated'
)

unconsolidated = Unit(
    layers=[
        [upper_splitter],
        [snow, upper_transparent],
        [upper_junction],
        [unsaturated],
        [lower_splitter],
        [slow, lag_fun],
        [lower_transparent, fast],
        [lower_junction],
    ],
    id='unconsolidated'
)

# Create the catchments
andelfingen = Node(
    units=[consolidated, unsaturated],
    weights=[0.24, 0.76],
    area=403.3,
    id='andelfingen'
)

appenzell = Node(
    units=[consolidated, unsaturated],
    weights=[0.92, 0.08],
    area=74.4,
    id='appenzell'
)

frauenfeld = Node(
    units=[consolidated, unsaturated],
    weights=[0.49, 0.51],
    area=134.4,
    id='frauenfeld'
)

halden = Node(
    units=[consolidated, unsaturated],
    weights=[0.34, 0.66],
    area=314.3,
    id='halden'
)

herisau = Node(
    units=[consolidated, unsaturated],
    weights=[0.88, 0.12],
    area=16.7,
    id='herisau'
)

jonschwil = Node(
    units=[consolidated, unsaturated],
    weights=[0.9, 0.1],
    area=401.6,
    id='jonschwil'
)

mogelsberg = Node(
    units=[consolidated, unsaturated],
    weights=[0.92, 0.08],
    area=88.1,
    id='mogelsberg'
)

mosnang = Node(
    units=[consolidated],
    weights=[1.0],
    area=3.1,
    id='mosnang'
)

stgallen = Node(
    units=[consolidated, unsaturated],
    weights=[0.87, 0.13],
    area=186.6,
    id='stgallen'
)

waengi = Node(
    units=[consolidated, unsaturated],
    weights=[0.63, 0.37],
    area=78.9,
    id='waengi'
)

# Create the network
thur_catchment = Network(
    nodes=[
        andelfingen,
        appenzell,
        frauenfeld,
        halden,
        herisau,
        jonschwil,
        mogelsberg,
        mosnang,
        stgallen,
        waengi,
    ],
    topography={
        'andelfingen': None,
        'appenzell': 'stgallen',
        'frauenfeld': 'andelfingen',
        'halden': 'andelfingen',
        'herisau': 'halden',
        'jonschwil': 'halden',
        'mogelsberg': 'jonschwil',
        'mosnang': 'jonschwil',
        'stgallen': 'halden',
        'waengi': 'frauenfeld',
    }
)

print('Done')