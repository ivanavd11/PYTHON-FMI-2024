class Material:
    """
    Define a material with a given mass and calculate its volume using a predefined density.
    """
    def __init__(self, mass):
        self.mass = mass
 
    @property
    def volume(self):
        return self.mass / self.DENSITY
 
 
class Concrete(Material):
    DENSITY = 2500
 
 
class Brick(Material):
    DENSITY = 2000
 
 
class Stone(Material):
    DENSITY = 1600
 
 
class Wood(Material):
    DENSITY = 600
 
 
class Steel(Material):
    DENSITY = 7700
 
 
class Factory:
    """
    Manage the creation and combination of materials while enforcing reuse and uniqueness rules.
    """
    _used_instances = []
 
    _dynamic_classes = {}
 
    _all_factories = []
 
    _all_base_materials = {
        "Concrete": Concrete,
        "Brick": Brick,
        "Stone": Stone,
        "Wood": Wood,
        "Steel": Steel,
    }
 
    def __init__(self):
        self._created_materials = []
        self._all_factories.append(self) 
 
    def __call__(self, *args, **kwargs):
        if not args and not kwargs:
            raise ValueError("Cannot have an instance without an argument or arguments.")
        if args and kwargs:
            raise ValueError("There cannot be an instance with a mixture of positional and named arguments.")
 
        if args:
            return self._create_from_args(*args)
        return self._create_from_kwargs(**kwargs)
 
    def _create_from_args(self, *args):
        if not self._validate_unused_materials(args):
            raise AssertionError("One or more materials have been used.")
        self._used_instances.extend(args)
 
        components = {}
 
        for material in args:
            material_name = material.__class__.__name__
            if material_name in self._all_base_materials.keys():
                components[material_name] = self._all_base_materials[material_name]
            else:
                class_components = material.__class__.__name__.split("_")
                for component_name in class_components:
                    components[component_name] = self._all_base_materials[component_name]
 
        class_name = "_".join(sorted(components.keys()))
 
        if class_name not in self._dynamic_classes.keys():
            self._create_dynamic_material(class_name, components)
 
        total_mass = 0
        for material in args:
            total_mass += material.mass
        new_material = self._dynamic_classes[class_name](total_mass)
        self._created_materials.append(new_material)
        return new_material
 
    def _create_from_kwargs(self, **kwargs):
        created_instances = []
        for name, mass in kwargs.items():
            if not self._validate_material_name(name):
                raise ValueError("Invalid material name")
            if name in self._all_base_materials:
                material_class = self._all_base_materials[name](mass)
                created_instances.append(material_class)
            elif name in self._dynamic_classes:
                material_class = self._dynamic_classes[name](mass)
                created_instances.append(material_class)
 
        self._created_materials.extend(created_instances)
        return tuple(created_instances)
 
    def _create_dynamic_material(self, name, components):
        total_density = 0
        for current in components.values():
            total_density += current.DENSITY
 
        if len(components):
            num_components = len(components)
        else:
            num_components = 1
        average_density = total_density / num_components

        dynamic_material = type(name,
                                (Material,), 
                                {
                                    'DENSITY': average_density 
                                }
                            )
        self._dynamic_classes[name] = dynamic_material
 
    def _validate_unused_materials(self, materials):
        return all(material not in self._used_instances for material in materials)
 
    def _validate_material_name(self, name):
        return name in self._all_base_materials or name in self._dynamic_classes
 
    def can_build(self, wall_volume):
        current_volume = 0
        for material in self._created_materials:
            if material not in self._used_instances:
                current_volume += material.volume
        return current_volume >= wall_volume
 
    @classmethod
    def can_build_together(cls, wall_volume):
        total_volume = 0
        for factory in cls._all_factories:
            for material in factory._created_materials:
                if material not in cls._used_instances:
                    total_volume += material.volume
        return total_volume >= wall_volume
    