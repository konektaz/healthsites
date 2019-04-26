__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '04/04/19'

from localities_osm.models.locality import LocalityOSMView, LocalityOSM


def get_all_osm_query():
    return LocalityOSMView.objects.filter(osm_id__isnull=False).exclude(name='')


def convert_into_osm_dict(locality):
    """Utility to convert old locality dict into osm dict.

    :param locality: Locality object.
    :type locality: localities.models.Locality

    """

    data = locality.repr_dict()

    osm_dict = data['values']
    osm_dict['name'] = data['name']

    if osm_dict.get('staff', None):
        staff = osm_dict['staff'].split('|')
        staff = [u'0' if v is u'' else v for v in staff]
        osm_dict['staff_doctors'] = staff[0]
        osm_dict['staff_nurses'] = staff[1]
        del osm_dict['staff']

    if osm_dict.get('inpatient_service', None):
        beds = osm_dict['inpatient_service'].split('|')
        beds = list(filter(None, beds))
        beds = [int(x) for x in beds]
        total_bed = sum(beds)
        osm_dict['inpatient_service'] = str(total_bed)

    for item, value in osm_dict.items():
        if '|' in value:
            value = value.split('|')
            osm_dict[item] = list(filter(None, value))

    return osm_dict


def split_osm_and_extension_attr(locality_attr):
    """Utility to split osm and extension attributes.

    :param locality_attr: Locality attributes.
    :type locality_attr: dict
        example: {
            "activities": [
                "medicine and medical specialties",
                "Maternal and women health",
                "pediatric care"
            ],
            "facility": "puskesmas",
            "notes": [
                "Outpatient consultation"
            ],
            "tags": [
                "general"
            ],
            "scope_of_service": [
                "specialized care",
                "general acute care",
                "rehabilitation care"
            ],
            "inpatient_service": "12",
            "staff_doctors": "8",
        }

    """

    osm_fields = LocalityOSM._meta.get_all_field_names()

    osm_attr = {}
    for field in osm_fields:
        if locality_attr.get(field, None):
            osm_attr[field] = locality_attr[field]
            del locality_attr[field]

    if locality_attr.get('defining_hours', None):
        del locality_attr['defining_hours']

    return osm_attr, locality_attr
