## Unit-safe measured quantitiesOriginally published: 2004-02-23 12:12:29 
Last updated: 2004-02-23 12:12:29 
Author: George Sakkis 
 
Programs that deal with measured quantities usually make an implicit assumption of the measurement unit, a practice which is error prone, inflexible and cumbersome. This metaclass solution takes the burden of dealing with measurement units from the user, by associating each quantity to a unit of some measure. Operations on instances of these measures are unit-safe; moreover, unit conversions take place implicitly.