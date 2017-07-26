import os
import os.path
import re

" RecipeUnpacker recreates a group of Python modules into current directory. "
" See http://code.activestate.com/recipes/577297-consolidate-group-of-modules-into-one-recipe/?in=lang-python "
__author__=["Jack Trainor (jacktrainor@gmail.com)",]
__version__="2010-07-23"
client_PY = """from shipping import *
import instance

class InstanceReactor(instance.Instance.Notifiee):
    def __init__(self, instance_):
        instance.Instance.Notifiee.__init__(self, instance_)
        
    def on_attribute(self, key):
        val = self.instance().attribute(key)
        print %DQ%InstanceReactor.%s : %s %s -> %s%DQ% % (%DQ%on_attribute%DQ%, self.instance().name(), key, val)
        
class TestReactor(InstanceReactor):
    def __init__(self, instance_):
        InstanceReactor.__init__(self, instance_)
        self.__key = %DQ%%DQ%
        self.__val = %DQ%%DQ%
        
    def on_attribute(self, key):
        self.__key = key
        self.__val = self.instance().attribute(key)
        
    def execute(self, key, val, result_=True):
        instance_ = self.instance()
        self.__key = %DQ%%DQ%
        self.__val = %DQ%%DQ%
        instance_.attribute_is(key, val)
        result = ((self.__key == key and self.__val == val) == result_)
        if not result:
            print %DQ%FAILED TestReactor.execute() %s %s: %s [%s] [%s]%DQ% % (instance_.type(), instance_.name(), key, val, self.__val)
        return result

class Tester(object):
    def __init__(self):
        self.__mgr = None
        self.__count = 0
        self.__successes = 0

    def setup(self):
        self.__mgr = instance.ShippingInstanceMgr()
        pass

    def takedown(self):
        self.__mgr = None

    def mgr(self):
        return self.__mgr

    def test(self, result):
        self.__count += 1
        if result:
            self.__successes += 1
        else:
            self.__successes += 0 # for breakpoint

    def test_bool(self, result, flag):
        self.test(result == flag)

    def test_instance_new(self, name_, type_):
        instance_ = self.mgr().instance_new(name_, type_)
        self.test(instance_ != None)
        if instance_:
            self.test(instance_.name() == name_)
            self.test(instance_.type() == type_)
        return instance_

    def test_attribute(self, instance_, key, val, flag=True):
        instance_.attribute_is(key, val)
        self.test_bool(instance_.attribute(key) == val, flag)

    def test_reactor(self, reactor, key, val, flag=True):
        result = reactor.execute(key, val)
        self.test_bool(result, flag)

    def test_readonly_attribute(self, instance_, key, expected):
        val = instance_.attribute(key)
        self.test(val == expected)

    def test_manager(self):
        self.setup()
        self.test(self.mgr() != None)
        self.takedown()

    def test_location(self):
        self.setup()
        a = %DQ%a%DQ%
        instance_ = self.test_instance_new(a, LOCATION_TYPE)
        self.test_readonly_attribute(instance_, LOC_SHIPMENT_COUNT_ATTR, %DQ%0%DQ%)
        self.takedown()

    def test_origin(self):
        self.setup()
        a = %DQ%a%DQ%
        instance_ = self.test_instance_new(a, ORIGIN_TYPE)
        reactor = TestReactor(instance_)
        self.takedown()

    def test_segment(self):
        self.setup()
        a = %DQ%a%DQ%
        instance_ = self.test_instance_new(a, SEGMENT_TYPE)
        self.test_attribute(instance_, SEG_SOURCE_ATTR, %DQ%xxx%DQ%)
        self.test_attribute(instance_, SEG_DESTINATION_ATTR, %DQ%xxx%DQ%)
        self.test_attribute(instance_, SEG_DISTANCE_ATTR, %DQ%10.00%DQ%)

        reactor = TestReactor(instance_)
        self.test_reactor(reactor, SEG_SOURCE_ATTR, %DQ%aaa%DQ%)
        self.test_reactor(reactor, SEG_DESTINATION_ATTR, %DQ%bbb%DQ%)
        self.test_reactor(reactor, SEG_DISTANCE_ATTR, %DQ%20.00%DQ%)

        self.takedown()

    def test_shipment(self):
        self.setup()
        a = %DQ%a%DQ%
        instance_ = self.test_instance_new(a, SHIPMENT_TYPE)
        self.test_attribute(instance_, SHP_DESTINATION_ATTR, %DQ%xxx%DQ%)
        self.test_attribute(instance_, SHP_ORIGIN_ATTR, %DQ%xxx%DQ%)
        self.test_attribute(instance_, SHP_LOCATION_ATTR, %DQ%xxx%DQ%)
        self.test_attribute(instance_, SHP_SEGMENT_ATTR, %DQ%xxx%DQ%)
        self.test_attribute(instance_, SHP_SPEED_ATTR, %DQ%2.00%DQ%)
        
        reactor = TestReactor(instance_)
        self.test_reactor(reactor, SHP_DESTINATION_ATTR, %DQ%yyy%DQ%)
        self.test_reactor(reactor, SHP_ORIGIN_ATTR, %DQ%yyy%DQ%)
        self.test_reactor(reactor, SHP_LOCATION_ATTR, %DQ%yyy%DQ%)
        self.test_reactor(reactor, SHP_SEGMENT_ATTR, %DQ%yyy%DQ%)
        self.takedown()

    def execute(self):
        print %DQ%Tester.execute()...%DQ%
        self.test_manager()
        self.test_location()
        self.test_origin()
        self.test_segment()
        self.test_shipment()

        self.report()

    def report(self):
        print %DQ%Tester:%DQ%, self.__successes, %DQ%out of%DQ%, self.__count,%DQ%tests.%DQ%
        if (self.__successes != self.__count):
            print %DQ%Tester: FAILED.%DQ%

def main():
    Tester().execute()
    raw_input(%DQ%Press RETURN...%DQ%)

if __name__ == %DQ%__main__%DQ%:
    print __file__
    main()
    
"""

engine_PY = """import sys
from shipping import *

class Engine(object):
    def __init__(self):
        self.__instance_eng = {}

    def instance_eng_new(self, name_, type_):
        import instance_eng
        import location
        import origin
        import segment
        import shipment
        
        instance_eng_ = self.instance_eng(name_)
        if not instance_eng_:
            if type_ == LOCATION_TYPE:
                instance_eng_ = location.Location(name_, type_, self)
            elif type_ == SEGMENT_TYPE:
                instance_eng_ = segment.Segment(name_, type_, self)
            elif type_ == SHIPMENT_TYPE:
                instance_eng_ = shipment.Shipment(name_, type_, self)
            elif type_ == ORIGIN_TYPE:
                instance_eng_ = origin.Origin(name_, type_, self)
            else:
                sys.stderr.write(%DQ%Engine.instance_eng_new: no such type %s.%SLASH%n%DQ% % type_)
            
            if instance_eng_:
                self.__instance_eng[name_] = instance_eng_
            else:
                sys.stderr.write(%DQ%Engine.instance_eng_new: failed to create %s of type %s.%SLASH%n%DQ% % (name_, type_))
        else:
            sys.stderr.write(%DQ%Engine.instance_eng_new: %s already exists.%SLASH%n%DQ% % name_)
        return instance_eng_
    
    def instance_eng(self, name_):
        instance_eng_ = self.__instance_eng.get(name_, None)
        return instance_eng_
    
    def instance_eng_del(self, name_):
        instance_eng_ = self.instance_eng(name_)
        if instance_eng_:
            del self.__instance_eng[name_]

"""

instance_PY = """import notifiee

def abstract(): # run-time emulation of C++ abstract method -- forces error if subclass doesn%SQ%t override
    import inspect
    caller = inspect.getouterframes(inspect.currentframe())[1][3]
    raise NotImplementedError(caller + %SQ% must be implemented in subclass%SQ%)

class Instance(object):
    def __init__(self, name_, type_):
        self.__name = name_
        self.__type = type_
        
    def name(self):
        return self.__name
    
    def type(self):
        return self.__type
    
    def attribute(self, key):           abstract()
    def attribute_is(self, key, val):   abstract()

    class Manager(object):
        def __init__(self):
            pass
        
        def instance(self, name_):              abstract()               
        def instance_new(self, name_, type_):   abstract()
        def instance_del(self, name_):          abstract()

    class Notifiee(notifiee.BaseNotifiee):
        def __init__(self, notifier_):
            notifiee.BaseNotifiee.__init__(self, notifier_)
        
        def instance(self):
            return self.notifier()
        
        def mgr(self):
            return self.instance().mgr()
        
        def on_attribute(self, key):           abstract()

    def last_notifiee_is(self, notifiee_):     abstract()
    def notifiee_is_not(self, notifiee_):      abstract()

def ShippingInstanceMgr():
    import instance_impl
    return instance_impl.ManagerImpl()

"""

instance_eng_PY = """from shipping import *
import notifiee
import instance

class InstanceEng(object):
    def __init__(self, name_, type_, engine_):
        self.__name = name_
        self.__type = type_
        self.__engine = engine_
    
    def name(self):
        return self.__name

    def type(self):
        return self.__type

    def engine(self):
        return self.__engine

"""

instance_impl_PY = """import sys
from shipping import *
import instance
import notifiee
import engine

class ManagerImpl(instance.Instance.Manager):
    def __init__(self):
        self.__instance = {}
        self.__engine = engine.Engine()
    
    def engine(self):
        return self.__engine 
    
    def activity_mgr(self):
        return self.engine().activity_mgr()
    
    def instance(self, name_):
        return self.__instance.get(name_, None)
            
    def instance_new(self, name_, type_):
        import location_rep
        import origin_rep
        import segment_rep
        import shipment_rep
        
        instance_ = self.instance(name_)        
        if not instance_:
            self.engine().instance_eng_new(name_, type_)
            if type_ == LOCATION_TYPE:
                instance_ = location_rep.LocationRep(name_, type_, self)
            elif type_ == ORIGIN_TYPE:
                instance_ = origin_rep.OriginRep(name_, type_, self)
            elif type_ == SEGMENT_TYPE:
                instance_ = segment_rep.SegmentRep(name_, type_, self)
            elif type_ == SHIPMENT_TYPE:
                instance_ = shipment_rep.ShipmentRep(name_, type_, self)
            else:
                sys.stderr.write(%DQ%ManagerImpl.instance_new: no such type %s.%SLASH%n%DQ% % type_)
            
            if instance_:
                self.__instance[name_] = instance_
            else:
                sys.stderr.write(%DQ%ManagerImpl.instance_new: failed to create %s of type %s.%SLASH%n%DQ% % (name_, type_))
        else:
            sys.stderr.write(%DQ%ManagerImpl.instance_new: %s already exists.%SLASH%n%DQ% % name_)
        return instance_       
    
    def instance_del(self, name_):
        instance_ = self.instance(name_)
        if instance_:
            del self.__instance[name_]
            self.engine().instance_eng_del(name_)

class InstanceImpl(instance.Instance):
    def __init__(self, name_, type_, mgr_):
        instance.Instance.__init__(self, name_, type_)
        self.__mgr = mgr_
        self.__name = name_
        self.__type = type_
        self.__notifiee = []
        
    def name(self):
        return self.__name
    
    def type(self):
        return self.__type
        
    def mgr(self):
        return self.__mgr
    
    def activity_mgr(self):
        return self.mgr().activity_mgr()
    
    def engine(self):
        return self.mgr().engine()
    
    def attribute(self, key):          notifiee.abstract()       
    def attribute_is(self, key, val):  notifiee.abstract()
    def on_attribute(self, key):
        for notifiee_ in self.__notifiee:
            notifiee_.on_attribute(key)

    def attribute_err(self, key):
        sys.stderr.write(%SQ%Can%SLASH%%SQ%t read %DQ%%s%DQ% attribute of %DQ%%s%DQ%%SLASH%n%SQ% % (key, self.name))

    def attribute_is_err(self, key, val):
        sys.stderr.write(%SQ%Can%SLASH%%SQ%t write %DQ%%s%DQ% to %s%DQ% attribute of %DQ%%s%DQ%%SLASH%n%SQ% % (val, key, self.name))

    def last_notifiee_is(self, notifiee_):
        self.__notifiee.append(notifiee_)
        
    def notifiee_is_not(self, notifiee_):
        self.__notifiee.remove(notifiee_)

if __name__ == %DQ%__main__%DQ%:
    print __file__

"""

location_PY = """from shipping import *
import notifiee
import engine
import instance_eng

class Location(instance_eng.InstanceEng):
    def __init__(self, name_, type_, engine_):
        instance_eng.InstanceEng.__init__(self, name_, type_, engine_)
        self.__shipment_count = 0 
        self.__notifiee = None

    def shipment_count(self):
        return self.__shipment_count
    
    def shipment_count_inc(self):
        self.shipment_count_is(self.__shipment_count + 1)
        
    def shipment_count_is(self, val):
        if self.__shipment_count != val:
            self.__shipment_count = val
            self.__notifiee.on_shipment_count()

    def last_notifiee_is(self, notifiee_):
        self.__notifiee = notifiee_
        
    def notifiee_is_not(self, notifiee_):
        if self.__notifiee == notifiee_:
            self.__notifiee = None

    class Notifiee(notifiee.OwnedNotifiee):
        def __init__(self, notifier_, owner_=None):
            notifiee.OwnedNotifiee.__init__(self, notifier_, owner_)

        def on_shipment_count(self):             notifiee.abstract()

"""

location_rep_PY = """from shipping import *
import instance_impl
import location

class LocationRep(instance_impl.InstanceImpl):
    def __init__(self, name_, type_, mgr_):
        instance_impl.InstanceImpl.__init__(self, name_, type_, mgr_)
        location_ = self.engine().instance_eng(name_)
        self.__locationReactor = LocationRep.LocationReactor(location_, self)
        
    def attribute(self, key):
        location_ = self.mgr().engine().instance_eng(self.name())
        if key is LOC_SHIPMENT_COUNT_ATTR:
            return str(location_.shipment_count())
        else:
            self.attribute_err(key)
        return %DQ%%DQ%

    def attribute_is(self, key, val):
        location_ = self.mgr().engine().instance_eng(self.name())
        self.attribute_is_err(key, val)
                        
    class LocationReactor(location.Location.Notifiee):
        def __init__(self, notifier_, location_rep_):
            location.Location.Notifiee.__init__(self, notifier_, location_rep_)
            
        def location_rep(self):
            return self.owner()

        def on_shipment_count(self):
            self.location_rep().on_attribute(LOC_SHIPMENT_COUNT_ATTR)



"""

notifiee_PY = """def abstract(): # run-time emulation of C++ abstract method -- forces error if subclass doesn%SQ%t override
    import inspect
    caller = inspect.getouterframes(inspect.currentframe())[1][3]
    raise NotImplementedError(caller + %SQ% must be implemented in subclass%SQ%)

class RootNotifiee:
    pass

class BaseNotifiee(RootNotifiee):
    def __init__(self, notifier_):
        self.__notifier = notifier_
        if notifier_:
            notifier_.last_notifiee_is(self)
            
    def notifier(self):
        return self.__notifier
    
    def notifierIs(self, notifier_):
        if self.__notifier != notifier_:
            if notifier_:
                notifier_.last_notifiee_is(None)
            self.__notifier = notifier_
            if notifier_:
                notifier_.last_notifiee_is(self)
                
class OwnedNotifiee(BaseNotifiee):
    def __init__(self, notifier_, owner_):
        BaseNotifiee.__init__(self, notifier_)
        self.__owner = owner_
            
    def owner(self):
        return self.__owner


"""

origin_PY = """from shipping import *
import notifiee
import engine
import location

class Origin(location.Location):
    def __init__(self, name_, type_, engine_):
        location.Location.__init__(self, name_, type_, engine_)
#        self.__shipment_arrived = %DQ%%DQ%
        self.__shipment_complete = %DQ%%DQ%
        self.__destination = %DQ%%DQ%
        self.__shipment_id = 0
        self.__notifiee = None

    def next_shipment_name(self):
        self.__shipment_id += 1
        return %DQ%%s:%s:%d%DQ% % (%DQ%Ship%DQ%, self.name(), self.__shipment_id)

    def destination(self):
        return self.__destination
    
    def destination_is(self, val):
        if self.__destination != val:
            self.__destination = val
            self.__notifiee.on_destination()
        
    def shipment_complete(self):
        return self.__shipment_complete
    
    def shipment_complete_is(self, val):
        if self.__shipment_complete != val:
            self.__shipment_complete = val
            self.__notifiee.on_shipment_complete()
            self.__shipment_complete = %DQ%%DQ%

    class Notifiee(notifiee.OwnedNotifiee):
        def __init__(self, notifier_, owner_):
            notifiee.OwnedNotifiee.__init__(self, notifier_, owner_)

        def on_shipment_arrived(self):   notifiee.abstract()

    def last_notifiee_is(self, notifiee_):
        if isinstance(notifiee_, Origin.Notifiee):
            self.__notifiee = notifiee_
        elif isinstance(notifiee_, location.Location.Notifiee):
            location.Location.last_notifiee_is(self, notifiee_)
        
    def notifiee_is_not(self, notifiee_):
        if isinstance(notifiee_, Origin.Notifiee):
            if self.__notifiee == notifiee_:
                self.__notifiee = None
        elif isinstance(notifiee_, location.Location.Notifiee):
            location.Location.notifiee_is_not(self, notifiee_)

"""

origin_rep_PY = """from shipping import *
import location_rep
import origin

class OriginRep(location_rep.LocationRep):
    def __init__(self, name_, type_, mgr_):
        location_rep.LocationRep.__init__(self, name_, type_, mgr_)
        origin_ = self.engine().instance_eng(name_)
        self.__originReactor = OriginRep.OriginReactor(origin_, self)

    def attribute(self, key):
        origin_ = self.mgr().engine().instance_eng(self.name())
        if key is ORG_DESTINATION_ATTR:
            return origin_.destination()
        elif key is ORG_NEXT_SHIPMENT_NAME_ATTR:
            return origin_.next_shipment_name()
        elif key is ORG_SHIPMENT_COMPLETE_ATTR:
            return origin_.shipment_complete()
        else:
            return location_rep.LocationRep.attribute(self, key)
        return %DQ%%DQ%
    
    def attribute_is(self, key, val):
        origin_ = self.mgr().engine().instance_eng(self.name())
        if key is ORG_DESTINATION_ATTR:
            origin_.destination_is(val)
        elif key is ORG_SHIPMENT_COMPLETE_ATTR:
            origin_.shipment_complete_is(val)
        else:
            location_rep.LocationRep.attribute_is(self, key, val)
                        
    class OriginReactor(origin.Origin.Notifiee):
        def __init__(self, notifier_, origin_rep_):
            origin.Origin.Notifiee.__init__(self, notifier_, origin_rep_)
            
        def origin_rep(self):
            return self.owner()
        
        def on_destination(self):
            self.origin_rep().on_attribute(ORG_DESTINATION_ATTR)

        def on_shipment_complete(self):
            self.origin_rep().on_attribute(ORG_SHIPMENT_COMPLETE_ATTR)


"""

segment_PY = """from shipping import *
import notifiee
import engine
import instance_eng

class Segment(instance_eng.InstanceEng):
    def __init__(self, name_, type_, engine_):
        instance_eng.InstanceEng.__init__(self, name_, type_, engine_)
        self.__source = %DQ%%DQ%
        self.__destination = %DQ%%DQ%
        self.__distance = 0
        self.__notifiee = None

    def source(self):
        return self.__source

    def source_is(self, val):
        if self.__source != val:
            self.__source = val
            self.__notifiee.on_source()

    def destination(self):
        return self.__destination

    def destination_is(self, val):
        if self.__destination != val:
            self.__destination = val
            self.__notifiee.on_destination()

    def distance(self):
        return self.__distance

    def distance_is(self, val):
        if self.__distance != val:
            self.__distance = val
            self.__notifiee.on_distance()

    def last_notifiee_is(self, notifiee_):
        self.__notifiee = notifiee_
        
    def notifiee_is_not(self, notifiee_):
        if self.__notifiee == notifiee_:
            self.__notifiee = None

    class Notifiee(notifiee.OwnedNotifiee):
        def __init__(self, notifier_, owner_):
            notifiee.OwnedNotifiee.__init__(self, notifier_, owner_)

        def on_source(self):            notifiee.abstract()
        def on_destination(self):       notifiee.abstract()
        def on_distance(self):          notifiee.abstract()


"""

segment_rep_PY = """from shipping import *
import instance_impl
import segment

class SegmentRep(instance_impl.InstanceImpl):
    def __init__(self, name_, type_, mgr_):
        instance_impl.InstanceImpl.__init__(self, name_, type_, mgr_)
        segment_ = self.engine().instance_eng(name_)
        self.__segmentReactor = SegmentRep.SegmentReactor(segment_, self)
        
    def attribute(self, key):
        segment_ = self.mgr().engine().instance_eng(self.name())
        if key == SEG_SOURCE_ATTR:
            return segment_.source()
        elif key == SEG_DESTINATION_ATTR:
            return segment_.destination()
        elif key == SEG_DISTANCE_ATTR:
            return %DQ%%.2f%DQ% % segment_.distance()
        else:
            self.attribute_err(key)
        return %DQ%%DQ%

    def attribute_is(self, key, val):
        segment_ = self.mgr().engine().instance_eng(self.name())
        if key == SEG_SOURCE_ATTR:
            segment_.source_is(val)
        elif key == SEG_DESTINATION_ATTR:
            segment_.destination_is(val)
        elif key == SEG_DISTANCE_ATTR:
            segment_.distance_is(float(val))
        else:
            self.attribute_is_err(key, val)

    class SegmentReactor(segment.Segment.Notifiee):
        def __init__(self, notifier_, segment_rep_):
            segment.Segment.Notifiee.__init__(self, notifier_, segment_rep_)
            
        def segment_rep(self):
            return self.owner()
        
        def on_source(self):
            self.segment_rep().on_attribute(SEG_SOURCE_ATTR)

        def on_destination(self):
            self.segment_rep().on_attribute(SEG_DESTINATION_ATTR)

        def on_distance(self):
            self.segment_rep().on_attribute(SEG_DISTANCE_ATTR)


"""

shipment_PY = """from shipping import *
import notifiee
import engine
import instance_eng

class Shipment(instance_eng.InstanceEng):
    def __init__(self, name_, type_, engine_):
        instance_eng.InstanceEng.__init__(self, name_, type_, engine_)  
        self.__destination = %DQ%%DQ%
        self.__origin = %DQ%%DQ%
        self.__location = %DQ%%DQ%
        self.__segment = %DQ%%DQ%
        self.__speed = 1.0
        self.__notifiee = None

    def destination(self):
        return self.__destination

    def destination_is(self, val):
        if self.__destination != val:
            self.__destination = val
            self.__notifiee.on_destination()

    def origin(self):
        return self.__origin

    def origin_is(self, val):
        if self.__origin != val:
            self.__origin = val
            self.__notifiee.on_origin()

    def location(self):
        return self.__location

    def location_is(self, val):
        if self.__location != val:
            self.__location = val
            location_ = self.engine().instance_eng(val)
            if location_:
                location_.shipment_count_inc()
            self.__notifiee.on_location()

    def segment(self):
        return self.__segment

    def segment_is(self, val):
        if self.__segment != val:
            self.__segment = val
            self.__notifiee.on_segment()
          
    def speed(self):
        return self.__speed

    def speed_is(self, val):
        if self.__speed != val:
            self.__speed = val
            self.__notifiee.on_speed()
          
    def last_notifiee_is(self, notifiee_):
        self.__notifiee = notifiee_
        
    def notifiee_is_not(self, notifiee_):
        if self.__notifiee == notifiee_:
            self.__notifiee = None

    class Notifiee(notifiee.OwnedNotifiee):
        def __init__(self, notifier_, owner_):
            notifiee.OwnedNotifiee.__init__(self, notifier_, owner_)

        def on_destination(self):   notifiee.abstract()
        def on_origin(self):   notifiee.abstract()
        def on_location(self):   notifiee.abstract()
        def on_segment(self):   notifiee.abstract()
        def on_speed(self):             notifiee.abstract()

"""

shipment_rep_PY = """from shipping import *
import instance_impl
import shipment

class ShipmentRep(instance_impl.InstanceImpl):
    def __init__(self, name_, type_, mgr_):
        instance_impl.InstanceImpl.__init__(self, name_, type_, mgr_)
        shipment_ = self.engine().instance_eng(name_)
        self.__shipmentReactor = ShipmentRep.ShipmentReactor(shipment_, self)

    def attribute(self, key):
        shipment_ = self.mgr().engine().instance_eng(self.name())
        if key == SHP_DESTINATION_ATTR:
            return shipment_.destination()
        elif key == SHP_ORIGIN_ATTR:
            return shipment_.origin()
        elif key == SHP_LOCATION_ATTR:
            return shipment_.location()
        elif key == SHP_SEGMENT_ATTR:
            return shipment_.segment()
        elif key == SHP_SPEED_ATTR:
            return %DQ%%.2f%DQ% % shipment_.speed()
        else:
            self.attribute_err(key)
        return %DQ%%DQ%

    def attribute_is(self, key, val):
        shipment_ = self.mgr().engine().instance_eng(self.name())
        if key == SHP_DESTINATION_ATTR:
            shipment_.destination_is(val)
        elif key == SHP_ORIGIN_ATTR:
            shipment_.origin_is(val)
        elif key == SHP_LOCATION_ATTR:
            shipment_.location_is(val)
        elif key == SHP_SEGMENT_ATTR:
            shipment_.segment_is(val)
        elif key == SHP_SPEED_ATTR:
            shipment_.speed_is(float(val))
        else:
            self.attribute_is_err(key, val)

                        
    class ShipmentReactor(shipment.Shipment.Notifiee):
        def __init__(self, notifier_, shipment_rep_):
            shipment.Shipment.Notifiee.__init__(self, notifier_, shipment_rep_)
            
        def shipment_rep(self):
            return self.owner()
        
        def on_destination(self):
            self.shipment_rep().on_attribute(SHP_DESTINATION_ATTR)

        def on_origin(self):
            self.shipment_rep().on_attribute(SHP_ORIGIN_ATTR)

        def on_location(self):
            self.shipment_rep().on_attribute(SHP_LOCATION_ATTR)

        def on_segment(self):
            self.shipment_rep().on_attribute(SHP_SEGMENT_ATTR)

        def on_speed(self):
            self.shipment_rep().on_attribute(SHP_SPEED_ATTR)


"""

shipping_PY = """LOCATION_TYPE = %DQ%Location%DQ%
LOC_SHIPMENT_COUNT_ATTR = %DQ%Shipment count%DQ%

ORIGIN_TYPE = %DQ%Origin%DQ%
ORG_DESTINATION_ATTR = %DQ%Destination%DQ%
ORG_NEXT_SHIPMENT_NAME_ATTR = %DQ%Next shipment name%DQ%
ORG_SHIPMENT_COMPLETE_ATTR = %DQ%Shipment complete%DQ%

SEGMENT_TYPE = %DQ%Segment%DQ%
SEG_SOURCE_ATTR = %DQ%Source%DQ%
SEG_DESTINATION_ATTR = %DQ%Destination%DQ%
SEG_DISTANCE_ATTR = %DQ%Distance%DQ%

SHIPMENT_TYPE = %DQ%Shipment%DQ%
SHP_DESTINATION_ATTR = %DQ%Destination%DQ%
SHP_ORIGIN_ATTR = %DQ%Origin%DQ%
SHP_LOCATION_ATTR = %DQ%Location%DQ%
SHP_SEGMENT_ATTR = %DQ%Segment%DQ%
SHP_SPEED_ATTR = %DQ%Speed%DQ%

"""


class RecipeUnpacker(object):
    SQUOTE_ESCAPE = "%SQ%"
    DQUOTE_ESCAPE = "%DQ%"
    SLASH_ESCAPE = "%SLASH%"
    TRIPLE_SQUOTE_ESCAPE = "%SQSQSQ%"
    TRIPLE_DQUOTE_ESCAPE = "%DQDQDQ%"
    def __init__(self, dir=None):
        self.dir = dir
        if not self.dir:
            self.dir = os.getcwd()            
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)

    def execute(self):
        os.chdir(self.dir)
        for key in globals():
            match = re.match(("^([A-Za-z0-9_]+)_PY$"), key)
            if match:
                file_name = "%s.py" % match.group(1)
                path = os.path.join(self.dir, file_name)
                print "Unpacking %s ..." % path 
                src = globals()[key]
                src = src.replace(RecipeUnpacker.TRIPLE_SQUOTE_ESCAPE, "'''")
                src = src.replace(RecipeUnpacker.TRIPLE_DQUOTE_ESCAPE, '"""')
                src = src.replace(RecipeUnpacker.SQUOTE_ESCAPE, "'")
                src = src.replace(RecipeUnpacker.DQUOTE_ESCAPE, '"')
                src = src.replace(RecipeUnpacker.SLASH_ESCAPE, "\\")
                open(path, "w").write(src)
        
if __name__ == "__main__":
    print __file__
    RecipeUnpacker().execute()
    raw_input("RecipeUnpacker complete. Press RETURN...") 
