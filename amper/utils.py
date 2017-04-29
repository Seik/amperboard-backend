import time

import random

import datetime
from rest_framework import serializers
from rest_framework.fields import empty


class RelationModelSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, data=empty, **kwargs):
        self.is_relation = kwargs.pop('is_relation', False)
        super(RelationModelSerializer, self).__init__(instance, data, **kwargs)

    def validate_empty_values(self, data):
        is_ok, data = super(RelationModelSerializer, self).validate_empty_values(data)
        if self.is_relation and not is_ok:
            model = getattr(self.Meta, 'model')
            model_pk = model._meta.pk.name

            if not isinstance(data, dict):
                error_message = self.default_error_messages['invalid'].format(datatype=type(data).__name__)
                raise serializers.ValidationError(error_message)

            if model_pk not in data:
                raise serializers.ValidationError({model_pk: model_pk + ' is required'})

            try:
                data = model.objects.get(pk=data[model_pk])
                return True, data
            except:
                raise serializers.ValidationError({model_pk: model_pk + ' is not valid'})
        return is_ok, data


def date_to_timestamp(d):
    return int(time.mktime(d.timetuple()))


def random_datetime(start, end):
    stime = date_to_timestamp(start)
    etime = date_to_timestamp(end)

    ptime = stime + random.random() * (etime - stime)

    return datetime.datetime.fromtimestamp(ptime)


def time_round(dt):
    a, b = divmod(round(dt.minute, -1), 60)
    return '%i:%02i' % ((dt.hour + a) % 24, b)
