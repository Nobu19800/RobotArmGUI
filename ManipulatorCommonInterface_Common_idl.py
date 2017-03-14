# Python stubs generated by omniidl from idl/ManipulatorCommonInterface_Common.idl
# DO NOT EDIT THIS FILE!

import omniORB, _omnipy
from omniORB import CORBA, PortableServer
_0_CORBA = CORBA


_omnipy.checkVersion(4,2, __file__, 1)

try:
    property
except NameError:
    def property(*args):
        return None


# #include "BasicDataType.idl"
import BasicDataType_idl
_0_RTC = omniORB.openModule("RTC")
_0_RTC__POA = omniORB.openModule("RTC__POA")

# #include "ManipulatorCommonInterface_DataTypes.idl"
import ManipulatorCommonInterface_DataTypes_idl
_0_JARA_ARM = omniORB.openModule("JARA_ARM")
_0_JARA_ARM__POA = omniORB.openModule("JARA_ARM__POA")

#
# Start of module "JARA_ARM"
#
__name__ = "JARA_ARM"
_0_JARA_ARM = omniORB.openModule("JARA_ARM", r"idl/ManipulatorCommonInterface_Common.idl")
_0_JARA_ARM__POA = omniORB.openModule("JARA_ARM__POA", r"idl/ManipulatorCommonInterface_Common.idl")


# enum AlarmType
_0_JARA_ARM.FAULT = omniORB.EnumItem("FAULT", 0)
_0_JARA_ARM.WARNING = omniORB.EnumItem("WARNING", 1)
_0_JARA_ARM.UNKNOWN = omniORB.EnumItem("UNKNOWN", 2)
_0_JARA_ARM.AlarmType = omniORB.Enum("IDL:JARA_ARM/AlarmType:1.0", (_0_JARA_ARM.FAULT, _0_JARA_ARM.WARNING, _0_JARA_ARM.UNKNOWN,))

_0_JARA_ARM._d_AlarmType  = (omniORB.tcInternal.tv_enum, _0_JARA_ARM.AlarmType._NP_RepositoryId, "AlarmType", _0_JARA_ARM.AlarmType._items)
_0_JARA_ARM._tc_AlarmType = omniORB.tcInternal.createTypeCode(_0_JARA_ARM._d_AlarmType)
omniORB.registerType(_0_JARA_ARM.AlarmType._NP_RepositoryId, _0_JARA_ARM._d_AlarmType, _0_JARA_ARM._tc_AlarmType)

# struct Alarm
_0_JARA_ARM.Alarm = omniORB.newEmptyClass()
class Alarm (omniORB.StructBase):
    _NP_RepositoryId = "IDL:JARA_ARM/Alarm:1.0"

    def __init__(self, code, type, description):
        self.code = code
        self.type = type
        self.description = description

_0_JARA_ARM.Alarm = Alarm
_0_JARA_ARM._d_Alarm  = (omniORB.tcInternal.tv_struct, Alarm, Alarm._NP_RepositoryId, "Alarm", "code", omniORB.tcInternal.tv_ulong, "type", omniORB.typeMapping["IDL:JARA_ARM/AlarmType:1.0"], "description", (omniORB.tcInternal.tv_string,0))
_0_JARA_ARM._tc_Alarm = omniORB.tcInternal.createTypeCode(_0_JARA_ARM._d_Alarm)
omniORB.registerType(Alarm._NP_RepositoryId, _0_JARA_ARM._d_Alarm, _0_JARA_ARM._tc_Alarm)
del Alarm

# typedef ... AlarmSeq
class AlarmSeq:
    _NP_RepositoryId = "IDL:JARA_ARM/AlarmSeq:1.0"
    def __init__(self, *args, **kw):
        raise RuntimeError("Cannot construct objects of this type.")
_0_JARA_ARM.AlarmSeq = AlarmSeq
_0_JARA_ARM._d_AlarmSeq  = (omniORB.tcInternal.tv_sequence, omniORB.typeMapping["IDL:JARA_ARM/Alarm:1.0"], 0)
_0_JARA_ARM._ad_AlarmSeq = (omniORB.tcInternal.tv_alias, AlarmSeq._NP_RepositoryId, "AlarmSeq", (omniORB.tcInternal.tv_sequence, omniORB.typeMapping["IDL:JARA_ARM/Alarm:1.0"], 0))
_0_JARA_ARM._tc_AlarmSeq = omniORB.tcInternal.createTypeCode(_0_JARA_ARM._ad_AlarmSeq)
omniORB.registerType(AlarmSeq._NP_RepositoryId, _0_JARA_ARM._ad_AlarmSeq, _0_JARA_ARM._tc_AlarmSeq)
del AlarmSeq

# typedef ... LimitSeq
class LimitSeq:
    _NP_RepositoryId = "IDL:JARA_ARM/LimitSeq:1.0"
    def __init__(self, *args, **kw):
        raise RuntimeError("Cannot construct objects of this type.")
_0_JARA_ARM.LimitSeq = LimitSeq
_0_JARA_ARM._d_LimitSeq  = (omniORB.tcInternal.tv_sequence, omniORB.typeMapping["IDL:JARA_ARM/LimitValue:1.0"], 0)
_0_JARA_ARM._ad_LimitSeq = (omniORB.tcInternal.tv_alias, LimitSeq._NP_RepositoryId, "LimitSeq", (omniORB.tcInternal.tv_sequence, omniORB.typeMapping["IDL:JARA_ARM/LimitValue:1.0"], 0))
_0_JARA_ARM._tc_LimitSeq = omniORB.tcInternal.createTypeCode(_0_JARA_ARM._ad_LimitSeq)
omniORB.registerType(LimitSeq._NP_RepositoryId, _0_JARA_ARM._ad_LimitSeq, _0_JARA_ARM._tc_LimitSeq)
del LimitSeq

# struct ManipInfo
_0_JARA_ARM.ManipInfo = omniORB.newEmptyClass()
class ManipInfo (omniORB.StructBase):
    _NP_RepositoryId = "IDL:JARA_ARM/ManipInfo:1.0"

    def __init__(self, manufactur, type, axisNum, cmdCycle, isGripper):
        self.manufactur = manufactur
        self.type = type
        self.axisNum = axisNum
        self.cmdCycle = cmdCycle
        self.isGripper = isGripper

_0_JARA_ARM.ManipInfo = ManipInfo
_0_JARA_ARM._d_ManipInfo  = (omniORB.tcInternal.tv_struct, ManipInfo, ManipInfo._NP_RepositoryId, "ManipInfo", "manufactur", (omniORB.tcInternal.tv_string,0), "type", (omniORB.tcInternal.tv_string,0), "axisNum", omniORB.typeMapping["IDL:JARA_ARM/ULONG:1.0"], "cmdCycle", omniORB.typeMapping["IDL:JARA_ARM/ULONG:1.0"], "isGripper", omniORB.tcInternal.tv_boolean)
_0_JARA_ARM._tc_ManipInfo = omniORB.tcInternal.createTypeCode(_0_JARA_ARM._d_ManipInfo)
omniORB.registerType(ManipInfo._NP_RepositoryId, _0_JARA_ARM._d_ManipInfo, _0_JARA_ARM._tc_ManipInfo)
del ManipInfo
_0_JARA_ARM.CONST_BINARY_00000001 = 1
_0_JARA_ARM.CONST_BINARY_00000010 = 2
_0_JARA_ARM.CONST_BINARY_00000100 = 4
_0_JARA_ARM.CONST_BINARY_00001000 = 8

# interface ManipulatorCommonInterface_Common
_0_JARA_ARM._d_ManipulatorCommonInterface_Common = (omniORB.tcInternal.tv_objref, "IDL:JARA_ARM/ManipulatorCommonInterface_Common:1.0", "ManipulatorCommonInterface_Common")
omniORB.typeMapping["IDL:JARA_ARM/ManipulatorCommonInterface_Common:1.0"] = _0_JARA_ARM._d_ManipulatorCommonInterface_Common
_0_JARA_ARM.ManipulatorCommonInterface_Common = omniORB.newEmptyClass()
class ManipulatorCommonInterface_Common :
    _NP_RepositoryId = _0_JARA_ARM._d_ManipulatorCommonInterface_Common[1]

    def __init__(self, *args, **kw):
        raise RuntimeError("Cannot construct objects of this type.")

    _nil = CORBA.Object._nil


_0_JARA_ARM.ManipulatorCommonInterface_Common = ManipulatorCommonInterface_Common
_0_JARA_ARM._tc_ManipulatorCommonInterface_Common = omniORB.tcInternal.createTypeCode(_0_JARA_ARM._d_ManipulatorCommonInterface_Common)
omniORB.registerType(ManipulatorCommonInterface_Common._NP_RepositoryId, _0_JARA_ARM._d_ManipulatorCommonInterface_Common, _0_JARA_ARM._tc_ManipulatorCommonInterface_Common)

# ManipulatorCommonInterface_Common operations and attributes
ManipulatorCommonInterface_Common._d_clearAlarms = ((), (omniORB.typeMapping["IDL:JARA_ARM/RETURN_ID:1.0"], ), None)
ManipulatorCommonInterface_Common._d_getActiveAlarm = ((), (omniORB.typeMapping["IDL:JARA_ARM/RETURN_ID:1.0"], omniORB.typeMapping["IDL:JARA_ARM/AlarmSeq:1.0"]), None)
ManipulatorCommonInterface_Common._d_getFeedbackPosJoint = ((), (omniORB.typeMapping["IDL:JARA_ARM/RETURN_ID:1.0"], omniORB.typeMapping["IDL:JARA_ARM/JointPos:1.0"]), None)
ManipulatorCommonInterface_Common._d_getManipInfo = ((), (omniORB.typeMapping["IDL:JARA_ARM/RETURN_ID:1.0"], omniORB.typeMapping["IDL:JARA_ARM/ManipInfo:1.0"]), None)
ManipulatorCommonInterface_Common._d_getSoftLimitJoint = ((), (omniORB.typeMapping["IDL:JARA_ARM/RETURN_ID:1.0"], omniORB.typeMapping["IDL:JARA_ARM/LimitSeq:1.0"]), None)
ManipulatorCommonInterface_Common._d_getState = ((), (omniORB.typeMapping["IDL:JARA_ARM/RETURN_ID:1.0"], omniORB.typeMapping["IDL:JARA_ARM/ULONG:1.0"]), None)
ManipulatorCommonInterface_Common._d_servoOFF = ((), (omniORB.typeMapping["IDL:JARA_ARM/RETURN_ID:1.0"], ), None)
ManipulatorCommonInterface_Common._d_servoON = ((), (omniORB.typeMapping["IDL:JARA_ARM/RETURN_ID:1.0"], ), None)
ManipulatorCommonInterface_Common._d_setSoftLimitJoint = ((omniORB.typeMapping["IDL:JARA_ARM/LimitSeq:1.0"], ), (omniORB.typeMapping["IDL:JARA_ARM/RETURN_ID:1.0"], ), None)

# ManipulatorCommonInterface_Common object reference
class _objref_ManipulatorCommonInterface_Common (CORBA.Object):
    _NP_RepositoryId = ManipulatorCommonInterface_Common._NP_RepositoryId

    def __init__(self, obj):
        CORBA.Object.__init__(self, obj)

    def clearAlarms(self, *args):
        return self._obj.invoke("clearAlarms", _0_JARA_ARM.ManipulatorCommonInterface_Common._d_clearAlarms, args)

    def getActiveAlarm(self, *args):
        return self._obj.invoke("getActiveAlarm", _0_JARA_ARM.ManipulatorCommonInterface_Common._d_getActiveAlarm, args)

    def getFeedbackPosJoint(self, *args):
        return self._obj.invoke("getFeedbackPosJoint", _0_JARA_ARM.ManipulatorCommonInterface_Common._d_getFeedbackPosJoint, args)

    def getManipInfo(self, *args):
        return self._obj.invoke("getManipInfo", _0_JARA_ARM.ManipulatorCommonInterface_Common._d_getManipInfo, args)

    def getSoftLimitJoint(self, *args):
        return self._obj.invoke("getSoftLimitJoint", _0_JARA_ARM.ManipulatorCommonInterface_Common._d_getSoftLimitJoint, args)

    def getState(self, *args):
        return self._obj.invoke("getState", _0_JARA_ARM.ManipulatorCommonInterface_Common._d_getState, args)

    def servoOFF(self, *args):
        return self._obj.invoke("servoOFF", _0_JARA_ARM.ManipulatorCommonInterface_Common._d_servoOFF, args)

    def servoON(self, *args):
        return self._obj.invoke("servoON", _0_JARA_ARM.ManipulatorCommonInterface_Common._d_servoON, args)

    def setSoftLimitJoint(self, *args):
        return self._obj.invoke("setSoftLimitJoint", _0_JARA_ARM.ManipulatorCommonInterface_Common._d_setSoftLimitJoint, args)

omniORB.registerObjref(ManipulatorCommonInterface_Common._NP_RepositoryId, _objref_ManipulatorCommonInterface_Common)
_0_JARA_ARM._objref_ManipulatorCommonInterface_Common = _objref_ManipulatorCommonInterface_Common
del ManipulatorCommonInterface_Common, _objref_ManipulatorCommonInterface_Common

# ManipulatorCommonInterface_Common skeleton
__name__ = "JARA_ARM__POA"
class ManipulatorCommonInterface_Common (PortableServer.Servant):
    _NP_RepositoryId = _0_JARA_ARM.ManipulatorCommonInterface_Common._NP_RepositoryId


    _omni_op_d = {"clearAlarms": _0_JARA_ARM.ManipulatorCommonInterface_Common._d_clearAlarms, "getActiveAlarm": _0_JARA_ARM.ManipulatorCommonInterface_Common._d_getActiveAlarm, "getFeedbackPosJoint": _0_JARA_ARM.ManipulatorCommonInterface_Common._d_getFeedbackPosJoint, "getManipInfo": _0_JARA_ARM.ManipulatorCommonInterface_Common._d_getManipInfo, "getSoftLimitJoint": _0_JARA_ARM.ManipulatorCommonInterface_Common._d_getSoftLimitJoint, "getState": _0_JARA_ARM.ManipulatorCommonInterface_Common._d_getState, "servoOFF": _0_JARA_ARM.ManipulatorCommonInterface_Common._d_servoOFF, "servoON": _0_JARA_ARM.ManipulatorCommonInterface_Common._d_servoON, "setSoftLimitJoint": _0_JARA_ARM.ManipulatorCommonInterface_Common._d_setSoftLimitJoint}

ManipulatorCommonInterface_Common._omni_skeleton = ManipulatorCommonInterface_Common
_0_JARA_ARM__POA.ManipulatorCommonInterface_Common = ManipulatorCommonInterface_Common
omniORB.registerSkeleton(ManipulatorCommonInterface_Common._NP_RepositoryId, ManipulatorCommonInterface_Common)
del ManipulatorCommonInterface_Common
__name__ = "JARA_ARM"

#
# End of module "JARA_ARM"
#
__name__ = "ManipulatorCommonInterface_Common_idl"

_exported_modules = ( "JARA_ARM", )

# The end.
