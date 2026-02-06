import copy
import datetime
from proj.models.model import Role


def convert(object):
    try:
        data = object.__dict__.copy()
        if data.get("_sa_instance_state", False):
            del data["_sa_instance_state"]

        if data.get("_sa_adapter", False):
            del data["_sa_adapter"]

        datetime_type = type(datetime.datetime(2022, 1, 1))
        date_type = type(datetime.date(2022, 1, 1))
        # data["lob"] = object.demand_request2.requestor_lob
        for (k, v) in data.items():
            if isinstance(v, datetime_type):
                data[k] = v.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(v, date_type):
                data[k] = v.strftime("%Y-%m-%d")
            elif k == 'roles':
                if v:
                    listRole = list()
                    for role in v:
                        listRole.append(convert(role))
                    data[k] = listRole

    except:
        data = {}

    return data


def convert_date(object):
    try:
        data = copy.deepcopy(object.__dict__)
        if data.get("_sa_instance_state", False):
            del data["_sa_instance_state"]

        if data.get("_sa_adapter", False):
            del data["_sa_adapter"]

        datetime_type = type(datetime.datetime(2022, 1, 1))
        date_type = type(datetime.date(2022, 1, 1))
        # data["lob"] = object.demand_request2.requestor_lob
        for (k, v) in data.items():

            if isinstance(v, datetime_type):
                data[k] = v.strftime("%d/%m/%Y %H:%M %p")
            elif isinstance(v, date_type):
                data[k] = v.strftime("%d/%m/%Y ")

    except:
        data = {}

    return data
