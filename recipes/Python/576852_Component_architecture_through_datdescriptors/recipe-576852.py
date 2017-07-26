def _get_combined_method(method_list):
    def new_func(*args, **kwargs):
        [m(*args, **kwargs) for m in method_list]
    return new_func

def component_method(func):
    """ method decorator """
    func._is_component_method = True
    return func

class Component(object):
    """ data descriptor """
    _is_component = True

    def __init__(self):
        self._cache = {}    # id(instance) -> component obj

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return self._cache.get(id(instance), None)

    def __set__(self, instance, value):
        self._cache[id(instance)] = value
        self._refresh_component_methods(instance)

    def __delete__(self, instance):
        # delete this instance from the cache
        del(self._cache[id(instance)])
        self._refresh_component_methods(instance)

    def _refresh_component_methods(self, instance):
        icls = instance.__class__
        # get all components defined in instance cls
        components = []
        for attr in dir(icls):
            obj = getattr(icls, attr)
            if getattr(obj, '_is_component', False):
                comp = getattr(instance, attr, None)
                if comp is not None:
                    components.append(comp)
        # clear all of the current instance _component_methods
        icms = getattr(instance, '_instance_component_methods', [])
        for meth in icms:
            delattr(instance, meth)
        # generate new set of instance component methods
        icms = {}
        for c in components:
            ccls = c.__class__
            for attr in dir(ccls):
                obj = getattr(ccls, attr)
                if getattr(obj, '_is_component_method', False):
                    if attr not in icms:
                        icms[attr] = []
                    icms[attr].append(getattr(c, attr))
        # also maintain the instance's class original functionality
        for attr, meths in icms.items():
            obj = getattr(icls, attr, None)
            if obj is not None:
                if callable(obj):
                    icms[attr].insert(0, getattr(instance, attr))
                else:
                    raise ValueError("Component method overrides attribute!")
        # assign the methods to the instance
        for attr, meths in icms.items():
            if len(meths) == 1:
                setattr(instance, attr, icms[attr][0])
            else:
                setattr(instance, attr, _get_combined_method(meths))
        # write all of the assigned methods in a list so we know which ones to
        # remove later
        instance._instance_component_methods = icms.keys()





if __name__ == "__main__":
    class Robot(object):
        firmware = Component()
        arm = Component()

        def power_on(self):
            print 'Robot.power_on'

        def kill_all_humans(self):
            """ demonstrates a method that components didn't take over """
            print 'Robot.kill_all_humans'

    class RobotFW(object):
        @component_method
        def power_on(self):
            print 'RobotFW.power_on'
            self.power_on_checks()

        def power_on_checks(self):
            """ demonstrates object encapsulation of methods """
            print 'RobotFW.power_on_checks'

    class UpgradedRobotFW(RobotFW):
        """ demonstrates inheritance of components possible """
        @component_method
        def laser_eyes(self, wattage):
            print "UpgradedRobotFW.laser_eyes(%d)" % wattage

    class RobotArm(object):
        @component_method
        def power_on(self):
            print 'RobotArm.power_on'

        @component_method
        def bend_girder(self):
            print 'RobotArm.bend_girder'


    r = Robot()
    print dir(r)
    r.power_on()
    print '-'*20 + '\n'

    r.firmware = RobotFW()
    print dir(r)
    r.power_on()
    print '-'*20 + '\n'

    print "try to bend girder (demonstrating adding a component)"
    try:
        r.bend_girder()
    except AttributeError:
        print "Could not bend girder (I have no arms)"
    print "adding an arm..."
    r.arm = RobotArm()
    print "try to bend girder"
    r.bend_girder()
    print dir(r)
    print '-'*20 + '\n'
    print "upgrading firmware (demonstrating inheritance)"
    r.firmware = UpgradedRobotFW()
    r.power_on()
    r.laser_eyes(300)

    del(r.firmware)
    try:
        r.laser_eyes(300)
    except AttributeError:
        print "I don't have laser eyes!"
