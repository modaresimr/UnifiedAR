# DataSet
## Dataset Format:
### Object:
    An object is a primitive object, a vector or in the form of a tuple of data components:
    Object ={o|     o is Primitive or
	                o=[o_1, ... , o_n] such that o_i is Object(Vector of object) or
	                o=(Prop_1, ... , Prop_n) forall i in {1...n}, Prop_i(o) is Object}
### Time Object:
Time might be a point, in case of an instantaneous event, or an interval during if it is durative. Supported durative time is range.

    time | [start_time:end_time]


### Event:
|Type|Actor| Time |
|-|-|-|
### Sensor Events:
|(Type, Value)|SensorId| Time |
|-|-|-|

### Activity Events:
|ActivityId|ActorId| Time |
|-|-|-|

### DataInformation:
#### Sensor Info
| Id | Name | Cumulative | OnChange | Nominal | Range | Location | Object | Sensor |
|-|-|-|-|-|-|-|-|-|



#### Activity Info
|Id|Name|
|-|-|




### File format: CSV
#### Sensor Info:
| Id | Name | Cumulative | OnChange | Nominal | Range | Location | Object | Sensor |
|-|-|-|-|-|-|-|-|-|
| int | string | bool | bool | bool | json {min,max}/{items} | string | string | string |
in case of nominal sensors, the range contain items and for numeric sensors, the range contain min and max

#### Sensor events:
|Type | Value | SensorId | Time |
|-|-|-|-|

#### Activity events:
|ActivityId|ActorId| StartTime | EndTime|
|-|-|-|-|

![](http://yuml.me/diagram/scruffy/class/[Preprocessing]->[Dispacher],[Dispacher]->[Segmentation],[Segmentation]->[FeatureExtraction],[FeatureExtraction]->[Classifier],[Classifier]->[Combiner],[Combiner]->[Evaluation])

