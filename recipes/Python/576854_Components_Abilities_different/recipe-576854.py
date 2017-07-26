# used for filtering out 'builtin' methods upon dir() of custom class
std_class_methods = dir(object)
std_instance_methods = dir(object())

# ------------- Components -------------------------------
class _ComponentAccessor(object):
    def __init__(self):
        # flags to prevent infinite recursion during obj '__get__'
        self._breaks = {}

    def __get__(self, instance, owner):
        # if an 'instance' is passed
        #   return dict of {component attr: component value}
        # else use 'owner'
        #   return dict of {component attr: component obj}
        if instance is None:
            obj = owner
        else:
            obj = instance
        if self._get_break(obj):
            return None
        self._set_break(obj)
        _d = {}
        attrs = [a for a in dir(owner) if a not in std_class_methods]
        for attr in attrs:
            component = getattr(owner, attr)
            if getattr(component, '_is_component', False):
                _d[attr] = getattr(obj, attr)
        self._release_break(obj)
        return _d

    def __set__(self, instance, value):
        raise ValueError("Cannot change a '_ComponentAccessor'")
    def __delete__(self, instance, value):
        raise ValueError("Cannot delete a '_ComponentAccessor'")

    def _get_break(self, obj):
        return self._breaks.get(id(obj), False)
    def _set_break(self, obj):
        self._breaks[id(obj)] = True
    def _release_break(self, obj):
        self._breaks[id(obj)] = False

class ClassWithComponents(object):
    """ inherit from this to provide component introspection """
    # introspection flag
    _utilizes_components = True
    # introspection 'property' (read only) that will return
    #   the class' current Components
    components = _ComponentAccessor()


class Component(object):
    """ the data descriptor to add to a class """
    _is_component = True

    def __init__(self, type=None):
        """ type - verify component is set to an instance
            of 'type' when assigned
        """
        self._type = type
        self._cache = {}    # TODO: make into weakref dict

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self._cache.get(id(instance), None)

    def __set__(self, instance, value):
        # check value against self._type
        if value is not None:
            if self._type is not None and not isinstance(value, self._type):
                raise TypeError("Invalid type '%s' for component! Needs to be '%s'" %\
                    (value.__class__.__name__, self._type.__name__,))
        self._cache[id(instance)] = value

    def __delete__(self, instance):
        del(self._cache[id(instance)])
# ------------- /Components ------------------------------



# ------------- Abilities --------------------------------
class _Ability(object):
    def __init__(self, method_name, *bound_methods):
        self.name = method_name
        # TODO: could look at method # of args, etc...
        self._methods = []
        for bm in bound_methods:
            self.append(bm)

    def __str__(self):
        return self.name

    def __call__(self, *args, **kwargs):
        if len(self._methods) == 0:
            return None
        elif len(self._methods) == 1:
            # only 1 method, return its return value
            return self._methods[0](*args, **kwargs)
        else:
            # call all of our methods in order, no return value
            for m in self._methods:
                m(*args, **kwargs)

    def __add__(self, other):
        if not isinstance(other, _Ability):
            raise TypeError("Can only add _Abilities together!")
        if other.name != self.name:
            raise ValueError("Abilities have mismatched names!")
        meth_list = self._methods + other._methods
        return _Ability(self.name, *meth_list)

    def append(self, bound_method):
        if bound_method in self._methods:
            raise ValueError("Cannot add duplicate methods to ability!")
        self._methods.append(bound_method)


class _AbilityAccessor(tuple):
    """ placeholder object for ability methods """
    def __new__(cls, abilities=None):
        if abilities is None:
            abilities = []
        # check for duplicate ability.names combine them
        _ab_d = {}
        for abil in abilities:
            if abil.name not in _ab_d:
                _ab_d[abil.name] = []
            _ab_d[abil.name].append(abil)
        abilities = []
        for name, ab_list in _ab_d.items():
            abil = ab_list.pop(0)
            for ab in ab_list:
                abil += ab
            abilities.append(abil)
        return tuple.__new__(cls, abilities)

    def __init__(self, abilities=None):
        tuple.__init__(self)
        # create a method on self to pass call onto ability
        # ignore passed in 'abilities' arg, use self
        for ab in self:
            object.__setattr__(self, ab.name, ab)

    def __add__(self, other):
        if isinstance(other, _AbilityAccessor):
            abs = tuple.__add__(self, other)
        elif isinstance(other, _Ability):
            abs = []
            abs.extend(self)
            abs.append(other)
        else:
            raise TypeError("Can only add to other _AbilityAccessors!")
        return _AbilityAccessor(abs)


class _AbilityLookup(object):
    def __init__(self):
        # dict of flags to prevent infinite recursion during '__get__'
        self._breaks = {}    # id(obj) -> True/False

    def __get__(self, instance, owner):
        # if an 'instance' is passed
        #   return dict of {ability attr: [ability value]}
        # else use 'owner'
        #   return dict of {ability attr: ability obj}
        _d = {}
        if instance is None:
            if self._get_break(owner):
                return None
            self._set_break(owner)
            attrs = [a for a in dir(owner) if a not in std_class_methods]
            for attr in attrs:
                obj = getattr(owner, attr)
                if getattr(obj, '_is_ability_method', False):
                    _d[attr] = obj
            self._release_break(owner)
            return _d
        else:
            if self._get_break(instance):
                return None
            self._set_break(instance)
            ability_accessor = _AbilityAccessor()
            attrs = [a for a in dir(instance) if a not in std_instance_methods]
            for attr in attrs:
                obj = getattr(instance, attr)
                # check if the obj is an ability method
                if getattr(obj, '_is_ability_method', False):
                    ability_accessor += _Ability(attr, obj)
                # else check if the obj is a class with abilities
                elif getattr(obj, '_utilizes_abilities', False):
                    # get that obj's abilities and extend ours
                    ability_accessor += obj.abilities
            self._release_break(instance)
            return ability_accessor

    def __set__(self, instance, value):
        raise ValueError("Cannot change an '_AbilityLookup'")
    def __delete__(self, instance, value):
        raise ValueError("Cannot delete an '_AbilityLookup'")

    def _get_break(self, obj):
        return self._breaks.get(id(obj), False)
    def _set_break(self, obj):
        self._breaks[id(obj)] = True
    def _release_break(self, obj):
        self._breaks[id(obj)] = False

def abilitymethod(func):
    """ method decorator to mark it as an 'abilitymethod' """
    # check if func has an 'invalid' name
    if func.func_name in dir(_AbilityAccessor):
        raise ValueError("Invalid name for an abilitymethod! '%s'" %\
                (func.func_name,))
    func._is_ability_method = True
    return func

class ClassWithAbilities(object):
    """ inherit from this to provide ability introspection """
    _utilizes_abilities = True
    abilities = _AbilityLookup()

# ------------- /Abilities -------------------------------


if __name__ == "__main__":
    class RobotFirmware(ClassWithAbilities):
        @abilitymethod
        def power_on(self):
            print 'RobotFirmware.power_on'
            self.power_on_checks()

        def power_on_checks(self):
            """ demonstrates object encapsulation of methods """
            print 'RobotFirmware.power_on_checks'

    class UpgradedRobotFirmware(RobotFirmware):
        @abilitymethod
        def laser_eyes(self, wattage):
            print "UpgradedRobotFirmware.laser_eyes(%d)" % wattage

    class RobotArm(ClassWithAbilities):
        @abilitymethod
        def power_on(self):
            print 'RobotArm.power_on'

        @abilitymethod
        def bend_girder(self):
            print 'RobotArm.bend_girder'



    class Robot(ClassWithComponents, ClassWithAbilities):
        firmware = Component(RobotFirmware)
        arm = Component()

        @abilitymethod
        def power_on(self):
            print 'Robot.power_on'

        def kill_all_humans(self):
            """ demonstrates a method that components didn't take over """
            print 'Robot.kill_all_humans'


    print '-- Components --------'
    print 'Robot.components:', Robot.components
    r = Robot()
    print 'r.components:    ', r.components
    print '\tuploading firmware to robot...'
    try:
        r.firmware  = RobotArm()
    except Exception, e:
        print "\tMALFUNCTION! %s" % (e,)
    print '\tuploading firmware to robot try #2...'
    r.firmware = RobotFirmware()
    print '\t...success'
    print 'r.components:    ', r.components
    del(r)
    print '----------------------'
    print ''
    print '-- Abilities ---------'
    print "Robot.abilities:", Robot.abilities
    r = Robot()
    print "r.abilities:    ", r.abilities
    print "r.abilities (by name): ", [ab.name for ab in r.abilities]
    print '\tuploading firmware to robot...'
    r.firmware = RobotFirmware()
    print "r.abilities (by name): ", [ab.name for ab in r.abilities]
    print "r.firmware.abilities:  ", r.firmware.abilities
    print '\tattaching arm to robot...'
    r.arm = RobotArm()
    print "r.abilities (by name): ", [ab.name for ab in r.abilities]
    print "\twhat abilities does 'UpgradedRobotFirmware' provide?"
    print "\t", [x for x in UpgradedRobotFirmware.abilities]
    print "\tOooh laser eyes! upgrading...",
    r.firmware = UpgradedRobotFirmware()
    print "...done"
    print "\tPowering on..."
    r.abilities.power_on()
    print "\tTesting out laser eyes"
    r.abilities.laser_eyes(300)
    print "\tDeleting firmware"
    r.firmware = None
    print "\tPowering on..."
    r.abilities.power_on()
    print '----------------------'
