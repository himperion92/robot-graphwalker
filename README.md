# robot-graphwalker
Graphwalker and Robot Framework integrated solution for Model Based Testing and Graphical Test Sequence design.

## Key Concepts

### Graphwalker
Open-source tool for executing tests based on sequence diagrams. Executes combinations of paths given a graphml file
and some set of functions which match by naming convention with graphml nodes and edges. [http://graphwalker.github.io/](http://graphwalker.github.io/)

### yED
Graph editor tool. Graphs can be exported in .graphml format that will be used as an input of graphwalker-based tools. [https://www.yworks.com/products/yed](https://www.yworks.com/products/yed)

### Robot Framework
Generic Python-native test automation tool. [https://robotframework.org/](https://robotframework.org/)

## Examples

_Example for `robot_graphic_seq`_:

_1.  Full test coverage:_
```
python -m robot_graphic_seq_cli -g robot-graphwalker/demo/models/coffee_machine_system.graphml -s full -t "Coffee System" -l "robot-graphwalker/demo/robot_libs/CoffeeMachineExtendedLibrary" -r reports
```

_2.  Randomized 50% coverage:_
```
python -m robot_graphic_seq_cli -g robot-graphwalker/demo/models/coffee_machine_system.graphml -s random -c 50 -t "Coffee System" -l "robot-graphwalker/demo/robot_libs/CoffeeMachineExtendedLibrary" -r reports
```

## Constraints
* Only Python2 compatible for the moment!
* Current version of `robot_graphic_seq` does not support Guards (conditions) within the edges, it does support Actions 
(arguments) tho. Nodes cannot contain neither Actions or Guards.
* Current version of `robot_graphic_seq` does not support test case documentation generation.
* Current version of `robot_graphic_seq` does not support specific path configuration.


