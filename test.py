from element import Element
from testeffect import TestEffect

testel = Element(5, 341)
testel.add_effect(TestEffect(341))

print(testel.get_universes())

out = testel.render(None, None)

print(out)